function refreshData(d, b, c) {
    var e = d;
    var f = "";
    var a = d.indexOf("?");
    if (a > 0) {
        e = d.substring(0, a);
        f = d.substring(a + 1)
    }
    if (b == null || b == "") {
        var a = d.indexOf("?SOURCECATALOGID=");
        if (a < 0) {
            a = d.indexOf("&SOURCECATALOGID=")
        }
        if (a > 0) {
            b = d.substring(a + "&SOURCECATALOGID=".length);
            a = b.indexOf("&");
            if (a > 0) {
                b = b.substring(0, a)
            }
        }
        if (b == null || b == "") {
            a = d.indexOf("?CATALOGID=");
            if (a < 0) {
                a = d.indexOf("&CATALOGID=")
            }
            if (a > 0) {
                b = d.substring(a + "&CATALOGID=".length);
                a = b.indexOf("&");
                if (a > 0) {
                    b = b.substring(0, a)
                }
            }
        }
    }
    if (f.indexOf("%SOURCEURL%") > 0) {
          if (c == null) {
              c = ""
          }
          c = c.replace(new RegExp(/&/g), "*_AND_*");
          c = c.replace(new RegExp(/\?/g), "*_QUESTION_*");
          c = c.replace(new RegExp(/ /g), "*_SPACE_*");
          console.log(f);
          f = f.replace(new RegExp(/%SOURCEURL%/g), "SOURCEURL=" + c)
    }
    var url = e;
    if (url.indexOf("?") > 0) {
        url += "&randnum=" + Math.random()
    } else {
        url += "?randnum=" + Math.random()
    }
    return {'url':url,'form':f,'header':{
      "Content-Type":"application/x-www-form-urlencoded; charset=utf-8"
    }};
}

function requestURL()
{
    var command = '/szseWeb/FrontController.szse?ACTIONID=7&%SOURCEURL%&SOURCECATALOGID=1110&CATALOGID=1743_detail_sme&TABKEY=tab1&DM=000001&site=main';
    var param = '/szseWeb/FrontController.szse?ACTIONID=7&AJAX=AJAX-TRUE&CATALOGID=1110&TABKEY=tab1&tab1PAGENO=1';
    var result = refreshData(command,null,param)
    console.log(result);

    var request = require('request');
    var domain = 'http://www.szse.cn';
    var  options = result;
    options.method = 'post';
    options.url = domain + options.url;
    request(options, function (err, res, body) {
        if (err) {
          console.log('请求失败:' + err);
        }else {
          console.log('请求完成:' + body);
        }
    });
}

var command = require("commander")
require("command-line-args")
require("JSON")

command.version("0.0.1")
    .option('-c, --command <string>', 'refresh command')
    .option('-p, --parament <string>', 'parament')
    .parse(process.argv);

// console.log(command.command);
// console.log(command.parament);
var ret = refreshData(command.command,null,command.param);
console.log(JSON.stringify(ret));
