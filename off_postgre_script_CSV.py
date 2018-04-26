from sqlalchemy import create_engine, Column, Integer, String, Sequence, Table, Text, ForeignKey, UniqueConstraint, PrimaryKeyConstraint, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import csv
import requests
import pdb

engine = create_engine('postgresql://hieutruong@localhost:5432/{}'.format('purbeurre', echo=False))


Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    url = Column(String(200))
    name = Column(Text)
    description = Column(Text)
    quantity = Column(String(100))
    brands = Column(String(100))
    nutrition_grade = Column(Float, default="NULL")
    main_category = Column(String(100))
    productImageUrl = Column(String(200))
    productImageThumbUrl = Column(String(200))
    __table_args__ = (
        UniqueConstraint('name', 'description', 'quantity'),
    )
    

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name_category = Column(String(100), unique=True)
    

class ProductCategory(Base):
    __tablename__ = 'products_categories'
    product_id = Column(Integer, ForeignKey('products.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    __table_args__ = (
        PrimaryKeyConstraint('product_id', 'category_id', name='uix_2'),
    )

Base.metadata.create_all(engine)


def productAdd(engine):
    apiProductsList = []
    with open("new_product.csv") as f:
        content = csv.reader(f, delimiter=";")
        index = 0
        for line in content:
            Session = sessionmaker(bind=engine)
            session = Session()
            productSpec = {}
            productSpec['url'] = line[0]
            productSpec['name'] = line[1]
            productSpec['description'] = line[2]
            productSpec['quantity'] = line[3]
            productSpec['brands'] = line[4]
            productSpec['nutrition_grade'] = line[9]
            productSpec['main_category'] = line[6]
            productSpec['productImageUrl'] = line[7]
            productSpec['productImageThumbUrl'] = line[8]
            productDbEntry = Product(**productSpec)
            try:
                session.merge(productDbEntry)
                session.commit()
            except:
                session.rollback()
            finally:
                index += 1
                print(index)
                categoriesAdd(productSpec, session, line)

def categoriesAdd(productSpec, session, line):
    try:
        productId = session.query(Product).filter_by(**productSpec).first().id
        print(productId)
        categoriesList = line[5].split(',')
        for category in categoriesList:
            print(category)
            categoryDbEntry = Category(name_category = category.strip())
            try:
                session.add(categoryDbEntry)
                session.commit()
            except:
                session.rollback()
            finally:
                categoryId = session.query(Category).filter_by(name_category = category.strip()).first().id
                productcategoryDbEntry = ProductCategory(product_id = productId, category_id = categoryId)
                try:
                    session.add(productcategoryDbEntry)
                    session.commit()
                except:
                    session.rollback()
                finally:
                    pass
    except:
        session.rollback()
        pass


def main():
    productAdd(engine)

if __name__ == "__main__":
    main()
