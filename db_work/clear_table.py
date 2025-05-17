from db_work.create_tables import Orders

import schedule
import time
import threading
from sqlalchemy.orm import sessionmaker
import logging


class TableCleaner:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)
        self.logger = logging.getLogger('table_cleaner')
        self.logger.setLevel(logging.INFO)

    def clear_table(self):
        session = self.Session()
        try:
            deleted_count = session.query(Orders).delete()
            session.commit()
            self.logger.info(f"Удалено {deleted_count} записей")
            return True
        except Exception as e:
            session.rollback()
            self.logger.error(f"Ошибка очистки: {e}")
            return False
        finally:
            session.close()

    def start(self):
        self.logger.info("Запуск сервиса очистки таблиц")
        schedule.every().day.at("16:00").do(self.clear_table)

        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)

        thread = threading.Thread(target=run_scheduler)
        thread.daemon = True
        thread.start()
