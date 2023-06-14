from repository.database import DataBase
from settings import ENVIRONMENT

class Migrator():
    def __init__(self, db:DataBase, migration_file = "migrations/migration.sql"):
        self.__db__ = db
        self.migration_file = migration_file
        
    def execute(self):
        print("[MIGRATION] Executing migration for => ", ENVIRONMENT)
        self.__db__.executeMigration(self.migration_file)
        print("[MIGRATION] Migration finish for => ", ENVIRONMENT)
        
        

if __name__ == '__main__':
    Migrator(DataBase("", env=ENVIRONMENT)).execute()
    