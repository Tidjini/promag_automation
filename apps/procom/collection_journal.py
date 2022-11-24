import time
from pathlib import Path
from datetime import datetime, timedelta

# application
from .window import Window
from .procom_io import ProcomIO
from .procom_image_converter import ProcomImageConverter
from .service import EncassiementServiceAPI

from .helpers import formalize
from .constants import *


assets = Path(__file__).parent.parent.parent / 'assets'
output = Path(__file__).parent.parent.parent / 'output'
search = assets / 'search.png'
now = datetime.now()


class CollectionJournal(Window):
    """Collection Journal Daily

    perform actions:
        - like open window
        - set start date
        - set end date
        - press the search button
        - close
    """

    _name = "Delivery status"

    @property
    def name(self):
        return self._name

    def search(self, period):
        end = f'{now:%d%m%Y}'
        start = now
        match period:
            case 'day':
                start = now
            case 'week':
                start = now.today() - timedelta(days=7)
            case 'month':
                start = now.today().replace(day=1)

        start = f'{start:%d%m%Y}'

        self.write(COLLECTION_START_DATE_LOCATION,  start)
        self.write(COLLECTION_END_DATE_LOCATION,  end)
        try:
            self.click_asset(str(search))
        except Exception as e:
            print('Exception ', e)
            pass

    def save_output(self, period):
        filename = f'collection_{period}'

        ProcomIO.save_simple(
            self, filename, ENCAISSEMNT_REGION, path=str(output))

    def convert_data(self, period):
        period_path = output / f'{period}.png'
        mtn, _ = ProcomImageConverter.convert(path=str(period_path))
        return mtn

    def save_to_service(self, period):
        filename = f'collection_{period}'
        mtn = self.convert_data(filename)
        print('mtn', mtn)
        if mtn[0] == '.':
            mtn = mtn[1:]

        # period_path = output / f'{period}.png'
        enc = {
            "reference": period,
            "label": period,
            "date_range": period,
            "value": float(mtn),
            "previous_value": 0.0
        }
        EncassiementServiceAPI.save("encaissements", enc)

    def perform_actions(self,  wait_time=20) -> None:
        """Perform Actions:

        Search with: Enter start date, end date with product ref, and press on search
        with sleep to wait for results (software performance 20s default)
        """

        with self as window:
            # wait 3sec to open
            time.sleep(3)
            for period in 'day', 'week', 'month':
                self.double_check()

                # if this window is not running go out
                if not window.is_running:
                    continue
                window.search(period)
                # wait untill get data
                time.sleep(wait_time)

                window.save_output(period)
                window.save_to_service(period)
