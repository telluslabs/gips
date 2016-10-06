import commands
import tempfile

# wget -L --user user --password password  http://e4ftl01.cr.usgs.gov/ASTT/AST_L1T.003/2002.05.11/AST_L1T_00305112002003107_20150426033306_21980.hdf.xml -O out.xml

def get(url, auth):
    outfile = tempfile.NamedTemporaryFile(delete=True)
    format = {'user': auth[0], 'password': auth[1], 'url': url, 'outfile': outfile.name}
    command = "wget -L --user {user} --password {password} {url} -O {outfile}".format(**format)
    status, output = commands.getstatusoutput(command)
    content = outfile.read()
    return content

if __name__ == "__main__":
    
    url = "http://e4ftl01.cr.usgs.gov/ASTT/AST_L1T.003/2002.05.11/AST_L1T_00305112002003107_20150426033306_21980.hdf.xml"
    content = get(url, ('bobbyhbraswell', 'Coffeedog_1'))
    print content
    
    url = "http://e4ftl01.cr.usgs.gov/ASTT/AST_L1T.003/2002.05.11"
    content = get(url, ('bobbyhbraswell', 'Coffeedog_1'))
    print content
