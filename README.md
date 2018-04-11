# Parse FDA Orange Book

Parse the [FDA Orange Book](https://www.accessdata.fda.gov/scripts/cder/ob/) into a Postgres database; a similar repo for the [Drugs@FDA database](https://www.accessdata.fda.gov/scripts/cder/daf/) is [also available](https://github.com/ConstantinoSchillebeeckx/parse_fda_drugs).

## To run

**NOTE:** project assumes python3

```
pip install -r requirements.txt
./run.sh
```

**NOTE:** 

- no foreign key constraints are established between tables.
- the table `products` lists some of the `approval_date` as 'Approved Prior to Jan 1, 1982', these entries have been converted to the date 'Jan 1, 1900' so that the table attribute can be setup as a date type.
- all table names and table attributes are formatted with underscores and lowercase; for example the table attribute `Drug_Product_Flag` is created as `drug_product_flag`.
- the archive [fda_orange_2018-04-09.zip](fda_orange_2018-04-09.zip) is provided as a refernce for a set of data that currently works with this repo; note that these data are otherwise updated on a **monthly basis**.
