from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey

# Connects to the database, for postgresql, had to install psycopg2 using
# pip3 install psycopg2-binary
engine = create_engine('postgresql://hieutruong@localhost:5432/test_off_script')

# template for tables
metadata = MetaData()
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('fullname', String),
              )

addresses = Table('addresses', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('user_id', None, ForeignKey('users.id')),
                  Column('email_address', String, nullable=False)
                 )

# actually creates the tables into the database
metadata.create_all(engine)



conn = engine.connect()
# possible to use exectutemany() for insert, update and delete options
# giving in a dictionnary