import mechanize
import cookielib

login_url = 'http://www.chess.com/login'

board_editor_url = 'http://www.chess.com/analysis-board-editor'

#curl "http://www.chess.com/api/get_diagram?id=new" -H "Host: www.chess.com" -H "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" -H "Accept-Language: fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3" -H "Accept-Encoding: gzip, deflate" -H "Cookie: __utma=1.883180574.1403634406.1414231346.1414233710.111; __utmz=1.1414233710.111.42.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __atuvc=0%7C39%2C1%7C40%2C4%7C41%2C3%7C42%2C14%7C43; fbtimeline_no_thanks=yes; PHPSESSID=5gl6kiuisvj1sq4kt9pfikfab2; __utmc=1; chess_mw_c16=0; fbm_429665630433565=base_domain=.chess.com; __atssc=reddit%3B1; __utmb=1.14.10.1414233710; fbsr_429665630433565=vnkz3CUp3a0rIECc7DgKd-UPAc4oanzNAV6h-_9PDts.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUURiZU4wLTJBdVV5dF9QTlJoME53UERRMThGWmZRWUltQ3ltUFBSc1dKSGtUNWFqT1BlR0V0VU5sRV8tWDJIM3d3eFZjWlFlaHhFU2Y0YUJlOTlPWEV6bm5PaThOV282NERYQXFqTmVHU2laY0dtZ2RlMG1LNTdjWGZWZXdDdWhuUmo5ek1xWTVuMjBwNndON3kyN21OZUpYQkJVdlFvdkJKNWROUG9jWWIxWkNPUWFoZ0ZxV2pIOGZmU0hmT0VsVDhhWjNZbVBVMVoyN096Mm90dTBiTzgxM3ZZd1RPbXpNZlIwQk9WZmg0VHZIWFRwYUNGSFVObWtWNTlVdjA0eXRCOFlScFhRZ0lSdU8taWlhMEtJZnJWeWVzODhvREl2ejExVW9Xa0lTUzlMZDdfNkctX0RqTWxuWHJBd1FnSjNYV0lWeEJTT3dDN20wV2F1UG1CVG5jWCIsImlzc3VlZF9hdCI6MTQxNDIzNDQyMiwidXNlcl9pZCI6IjY0OTczMzk0MiJ9; __atuvs=544b7f469808815d003; __utmt=1; __utma=56795640.1435373170.1414234626.1414234626.1414234626.1; __utmb=56795640.1.10.1414234626; __utmc=56795640; __utmz=56795640.1414234626.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)" -H "Connection: keep-alive" -H "If-Modified-Since: Sat, 25 Oct 2014 10:58:51 GMT"
get_new_diagram_id_url = "http://www.chess.com/api/get_diagram?id=new"


# curl "http://www.chess.com/api/get_diagram" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" -H "Accept-Encoding: gzip, deflate" -H "Accept-Language: fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3" -H "Cache-Control: no-cache" -H "Connection: keep-alive" -H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" -H "Cookie: __utma=1.883180574.1403634406.1414231346.1414233710.111; __utmz=1.1414233710.111.42.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __atuvc=0%7C39%2C1%7C40%2C4%7C41%2C3%7C42%2C14%7C43; fbtimeline_no_thanks=yes; PHPSESSID=5gl6kiuisvj1sq4kt9pfikfab2; __utmc=1; chess_mw_c16=0; fbm_429665630433565=base_domain=.chess.com; __atssc=reddit%3B1; __utmb=1.14.10.1414233710; fbsr_429665630433565=vnkz3CUp3a0rIECc7DgKd-UPAc4oanzNAV6h-_9PDts.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUURiZU4wLTJBdVV5dF9QTlJoME53UERRMThGWmZRWUltQ3ltUFBSc1dKSGtUNWFqT1BlR0V0VU5sRV8tWDJIM3d3eFZjWlFlaHhFU2Y0YUJlOTlPWEV6bm5PaThOV282NERYQXFqTmVHU2laY0dtZ2RlMG1LNTdjWGZWZXdDdWhuUmo5ek1xWTVuMjBwNndON3kyN21OZUpYQkJVdlFvdkJKNWROUG9jWWIxWkNPUWFoZ0ZxV2pIOGZmU0hmT0VsVDhhWjNZbVBVMVoyN096Mm90dTBiTzgxM3ZZd1RPbXpNZlIwQk9WZmg0VHZIWFRwYUNGSFVObWtWNTlVdjA0eXRCOFlScFhRZ0lSdU8taWlhMEtJZnJWeWVzODhvREl2ejExVW9Xa0lTUzlMZDdfNkctX0RqTWxuWHJBd1FnSjNYV0lWeEJTT3dDN20wV2F1UG1CVG5jWCIsImlzc3VlZF9hdCI6MTQxNDIzNDQyMiwidXNlcl9pZCI6IjY0OTczMzk0MiJ9; __atuvs=544b7f469808815d003; __utmt=1; __utma=56795640.1435373170.1414234626.1414234626.1414234626.1; __utmb=56795640.1.10.1414234626; __utmc=56795640; __utmz=56795640.1414234626.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)" -H "Host: www.chess.com" -H "Pragma: no-cache" -H "Referer: http://www.chess.com/analysis-board-editor" -H "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0" --data "id=2256802&text_setup=%26-diagramtype%3A%0AchessGame%0A%26-colorscheme%3A%0Ablue%0A%26-piecestyle%3A%0Aclassic%0A%26-float%3A%0Aleft%0A%26-flip%3A%0Afalse%0A%26-prompt%3A%0Afalse%0A%26-coords%3A%0Afalse%0A%26-size%3A%0A45%0A%26-lastmove%3A%0A%0A%26-focusnode%3A%0A%0A%26-beginnode%3A%0A%0A%26-endnode%3A%0A%0A%26-hideglobalbuttons%3A%0Afalse%0A%26-pgnbody%3A%0A%5BEvent%20%22Live%20Chess%22%5D%0A%5BSite%20%22Chess.com%22%5D%0A%5BDate%20%222014.10.18%22%5D%0A%5BWhite%20%22pilipolio%22%5D%0A%5BBlack%20%22vpmishra2003%22%5D%0A%5BResult%20%220-1%22%5D%0A%5BWhiteElo%20%22987%22%5D%0A%5BBlackElo%20%22979%22%5D%0A%5BTimeControl%20%225%7C2%22%5D%0A%5BTermination%20%22vpmishra2003%20won%20on%20time%22%5D%0A%0A1.d4%20d5%202.c4%20dxc4%203.e4%20e6%204.Bxc4%20h6%205.Nf3%20Nf6%206.Nc3%20Bd7%207.O-O%20Nc6%208.Bf4%20Bb4%209.Re1%20Bxc3%2010.bxc3%20Nh5%2011.Be3%20Qe7%2012.d5%20exd5%2013.Bxd5%20O-O-O%2014.Qb3%20Nf6%2015.Rab1%20b6%2016.Nd4%20Nxd5%2017.exd5%20Nxd4%2018.Bxd4%20Qg5%2019.a4%20Bf5%2020.Rb2%20Rhe8%2021.Rbe2%20Rxe2%2022.Rxe2%20Qc1%2B%20%0A0-1"
post_diagram_url = 'http://www.chess.com/api/get_diagram'

browser = mechanize.Browser()
# fixes HTTP Error 403: request disallowed by robots.txt?
browser.set_handle_robots(False)

# Cookie Jar
cj = cookielib.LWPCookieJar()
browser.set_cookiejar(cj)

# Browser options
browser.set_handle_equiv(True)
browser.set_handle_gzip(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
browser.set_debug_http(True)
browser.set_debug_redirects(True)
browser.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0'),
('X-Requested-With', 'XMLHttpRequest')]

browser.open(login_url)
#raise ''
browser.select_form(nr = 0)
browser.form['c1'] = 'pilipolio'
browser.form['loginpassword'] = 'mallin50CC'
#browser.form.new_control(type='hidden', name='Qform__FormControl', attrs={}, ignore_unknown=False, select_default=False, index=None)

# triggers some js adding other controls to the form before submitting
# so browser.form.click('btnLogin') does nothing
""" qc.pB('LoginForm', 'btnLogin', 'QClickEvent', '')
 pB => postBack: function(strForm, strControl, strEvent, strParameter)
postBack: function(strForm, strControl, strEvent, strParameter) {
	var strForm = $j("#Qform__FormId").attr("value");
	var objForm = $j('#' + strForm);

	$j('#Qform__FormControl').attr("value", strControl);
	$j('#Qform__FormEvent').attr("value", strEvent);
	$j('#Qform__FormParameter').attr("value", strParameter);
	$j('#Qform__FormCallType').attr("value", "Server");
	$j('#Qform__FormUpdates').attr("value", this.formUpdates());
	$j('#Qform__FormCheckableControls').attr("value", this.formCheckableControls(strForm, "Server"));

	// have $j trigger the submit event (so it can catch all submit events)
	objForm.trigger("submit");
}
"""

addition_inputs = {
    'Qform__FormControl': 'btnLogin',
    'Qform__FormEvent': 'QClickEvent',
    #'Qform__FormParameter': '',
    'Qform__FormCallType': 'Server',
    #'Qform__FormUpdates': '',
    'Qform__FormCheckableControls': 'rememberme',
    #'Qform__FormState': '0dec296d10463d0733295bba03be1e19'
    #'Qform__FormId': 'LoginForm'
    }

# the request need to have the js added data
# login_request.get_data()
login_request = browser.form.click('btnLogin')
#addition_inputs = {'Qform__FormCheckableControls': 'rememberme'}
def to_data(params, equal='=', sep='&'):
    return sep.join("{}{}{}".format(k,equal, v) for k, v in params.items())
    
login_request.add_data(login_request.get_data() + '&' + to_data(addition_inputs))

with open('login_request.html', 'w') as f:
    f.write(login_request.get_data())

login_submit_response = browser.open(login_request)
with open('login_response.html', 'w') as f:
    f.write(login_submit_response.get_data())

#login_submit_response = browser.submit()
#with open('login_response.html', 'w') as f:
#    f.write(login_submit_response.get_data())

board_editor_response = browser.open(board_editor_url)
with open('board_editor_response.html', 'w') as f:
    f.write(board_editor_response.get_data())

new_diagram_id = int(browser.open(get_new_diagram_id_url).get_data())

print "new_diagram_id = {}".format(new_diagram_id)

with open("D:\chess_screenshot\pilipolio_vs_jollyr_2014_10_24.pgn") as f:
    pgn_text = f.read().replace('\n','')
pgn_text = '1.d4%20d5'

#--data "id=2256802&text_setup=%26-diagramtype%3A%0AchessGame%0A%26-colorscheme%3A%0Ablue%0A%26-piecestyle%3A%0Aclassic%0A%26-float%3A%0Aleft%0A%26-flip%3A%0Afalse%0A%26-prompt%3A%0Afalse%0A%26-coords%3A%0Afalse%0A%26-size%3A%0A45%0A%26-lastmove%3A%0A%0A%26-focusnode%3A%0A%0A%26-beginnode%3A%0A%0A%26-endnode%3A%0A%0A%26-hideglobalbuttons%3A%0Afalse%0A%26-pgnbody%3A%0A%5BEvent%20%22Live%20Chess%22%5D%0A%5BSite%20%22Chess.com%22%5D%0A%5BDate%20%222014.10.18%22%5D%0A%5BWhite%20%22pilipolio%22%5D%0A%5BBlack%20%22vpmishra2003%22%5D%0A%5BResult%20%220-1%22%5D%0A%5BWhiteElo%20%22987%22%5D%0A%5BBlackElo%20%22979%22%5D%0A%5BTimeControl%20%225%7C2%22%5D%0A%5BTermination%20%22vpmishra2003%20won%20on%20time%22%5D%0A%0A1.d4%20d5%202.c4%20dxc4%203.e4%20e6%204.Bxc4%20h6%205.Nf3%20Nf6%206.Nc3%20Bd7%207.O-O%20Nc6%208.Bf4%20Bb4%209.Re1%20Bxc3%2010.bxc3%20Nh5%2011.Be3%20Qe7%2012.d5%20exd5%2013.Bxd5%20O-O-O%2014.Qb3%20Nf6%2015.Rab1%20b6%2016.Nd4%20Nxd5%2017.exd5%20Nxd4%2018.Bxd4%20Qg5%2019.a4%20Bf5%2020.Rb2%20Rhe8%2021.Rbe2%20Rxe2%2022.Rxe2%20Qc1%2B%20%0A0-1"
#id=2257116&text_setup=%26-lastmove%3A%26-beginnode%3A%26-float%3Aleft%26-size%3A45%26-endnode%3A%26-coords%3Afalse%26-hideglobalbuttons%3Afalse%26-focusnode%3A%26-colorscheme%3Ablue%26-pgnbody%3A1.d4%2520d5%26-prompt%3Afalse%26-diagramtype%3AchessGame%26-flip%3Afalse%26-piecestyle%3Aclassic'

import urllib

post_diagram_data = to_data({
    'id': new_diagram_id,
    'text_setup': urllib.quote('&' + to_data({
        '-diagramtype': '\nchessGame\n',
        '-colorscheme': '\nblue\n',
        '-piecestyle': '\nclassic\n',
        '-float': '\nleft\n',
        '-flip': '\nfalse\n',
        '-prompt': '\nfalse\n',
        '-coords': '\nfalse\n',
        '-size': '\n45\n',
        '-lastmove': '\n\n',
        '-focusnode': '\n\n',
        '-beginnode': '\n\n',
        '-endnode': '\n\n',
        '-hideglobalbuttons': '\nfalse\n',
        '-pgnbody': '\n1.d4 Nf6'}, equal=':'))
        })
    
request = mechanize.Request(post_diagram_url)
request.method = 'POST'
request.add_data(post_diagram_data)
#request.add_data("id=" + str(new_diagram_id) + "&text_setup=%26-diagramtype%3A%0AchessGame%0A%26-colorscheme%3A%0Ablue%0A%26-piecestyle%3A%0Aclassic%0A%26-float%3A%0Aleft%0A%26-flip%3A%0Afalse%0A%26-prompt%3A%0Afalse%0A%26-coords%3A%0Afalse%0A%26-size%3A%0A45%0A%26-lastmove%3A%0A%0A%26-focusnode%3A%0A%0A%26-beginnode%3A%0A%0A%26-endnode%3A%0A%0A%26-hideglobalbuttons%3A%0Afalse%0A%26-pgnbody%3A%0A%5BEvent%20%22Live%20Chess%22%5D%0A%5BSite%20%22Chess.com%22%5D%0A%5BDate%20%222014.10.18%22%5D%0A%5BWhite%20%22pilipolio%22%5D%0A%5BBlack%20%22vpmishra2003%22%5D%0A%5BResult%20%220-1%22%5D%0A%5BWhiteElo%20%22987%22%5D%0A%5BBlackElo%20%22979%22%5D%0A%5BTimeControl%20%225%7C2%22%5D%0A%5BTermination%20%22vpmishra2003%20won%20on%20time%22%5D%0A%0A1.d4%20d5%202.c4%20dxc4%203.e4%20e6%204.Bxc4%20h6%205.Nf3%20Nf6%206.Nc3%20Bd7%207.O-O%20Nc6%208.Bf4%20Bb4%209.Re1%20Bxc3%2010.bxc3%20Nh5%2011.Be3%20Qe7%2012.d5%20exd5%2013.Bxd5%20O-O-O%2014.Qb3%20Nf6%2015.Rab1%20b6%2016.Nd4%20Nxd5%2017.exd5%20Nxd4%2018.Bxd4%20Qg5%2019.a4%20Bf5%2020.Rb2%20Rhe8%2021.Rbe2%20Rxe2%2022.Rxe2%20Qc1%2B%20%0A0-1")
post_diagram_response = browser.open(request)
with open('post_diagram_response.html', 'w') as f:
    f.write(post_diagram_response.get_data())

