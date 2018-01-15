
Right now most products are supported.  Rerun gips installation
faff to get the AWS API library you need:

```
$ . venv/bin/activate # if needed
(venv) $ pip install -r requirements.txt
```

It also won't work unless you have API access to AWS:

https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/

Provide the special access tokens via env var (again, for now):

```
export AWS_ACCESS_KEY_ID='your-id'
export AWS_SECRET_ACCESS_KEY='your-key'
```

Finally set `settings.py` to tell gips to fetch C1 assets from S3:

```
REPOS = {
    'landsat': {
        # . . .
        'source': 's3', # default is 'usgs'
    }
}
```

After this is done, `gips_inventory --fetch`, `gips_inventory`, and
`gips_process -p ref-toa ndvi-toa` should work for S3 assets.
