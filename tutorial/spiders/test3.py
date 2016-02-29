from StringIO import StringIO
import gzip
import urllib2
url='http://te.hotel.qunar.com/render/detailV2.jsp?HotelSEQ=shanghai_city_3551&cityurl=shanghai_city&fromDate=2015-07-02&toDate=2015-07-04&basicData=1&lastupdate=-1&requestID=a588ce2-mq61v-afvp&mixKey=1399c69f45a0bc3c3f19b0d143575548220624y9Kjgh7a3x1iyLfDYGEwblONgC42uhZX5V6p&roomId=&filterid=db444c6d-3ce2-42c9-95af-189e90b7ed20_A&QUFP=ZSS_A7000117&isNewBook=1&showRestricted=&QUCP=ZSD_171F874F&v=1435755481427&cn=1&u=-FsNxpHjDX8pbTdb5HEBe5mY1n1pk5wrrmf1fh1cn14ifqqvm6ebwo0mr439h6&__jscallback=jQuery183016604609554633498_1435755480778&_=1435755481440'

request = urllib2.Request(url)
request.add_header('Accept-encoding', 'gzip')
response = urllib2.urlopen(request)
if response.info().get('Content-Encoding') == 'gzip':
    buf = StringIO( response.read())
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()
    print data