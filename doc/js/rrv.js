const server_name = ["strasserad","vaultish","bridgehead","gold"];

//CSVファイルを読み込む
function getCSV(date1, date2, server, job) {
    url1 = "https://sokomin.github.io/RS-Ranking/out/jpn_lv/" + date1 + "_" + server_name[server] + "_" + job + ".csv";
    url2 = "https://sokomin.github.io/RS-Ranking/out/jpn_lv/" + date2 + "_" + server_name[server] + "_" + job + ".csv";

    var request = [
        { url: url1 },
        { url: url2 },
        // { url: 'hoge04.json', params: { hoge: 615, huga: 2280 } }
    ];
    
    var jqXHRList = [];
    
    for (var i = 0; i < request.length; i++) {
        jqXHRList.push($.ajax({ // $.ajaxの戻り値を配列に格納
            url: request[i].url,
            // data: request[i].params,
            type: 'GET',
            // dataType: 'json'
        }));
    }
    
    // $.when関数を利用する
    // $.whenは可変長引数を取るので、apllyメソッドを利用して配列で渡せるようにする
    // $.whenのコンテキスト(applyの第一引数)はjQueryである必要があるので $ を渡す
    $.when.apply($, jqXHRList).done(function () {
        var csv_data = [];
        var statuses = [];
        var jqXHRResultList = [];
        // 結果は仮引数に可変長で入る **順番は保証されている**
        // 取り出すには arguments から取り出す
        // さらにそれぞれには [data, textStatus, jqXHR] の配列になっている
        for (var i = 0; i < arguments.length; i++) {
            var result = arguments[i];
            csv_data.push(result[0]);
            statuses.push(result[1]);
            jqXHRResultList.push(result[3]);
        }
    
        console.log(csv_data);// => リクエストの配列と同じ順番で結果を参照できる
        convertCSVtoArray(csv_data);

    });
}

var obj_format = {0: "rank", 1: "img",2: "job", 3:"name", 4:"lv", 5:"returner"};
var rank_now = {};
var rank_comp = {};

// 読み込んだCSVデータをオブジェクトに変換
function convertCSVtoArray(csv_data) {// 読み込んだCSVデータが文字列として渡される
    // 初期化
    // obj_format = {};
    rank_now = {};
    rank_comp = {};

    var result = [];// 最終的な二次元配列を入れるための配列
    var tmp = csv_data[0].split("\n");// 改行を区切り文字として行を要素とした配列を生成
    // 各行ごとにカンマで区切った文字列を要素とした二次元配列を生成
    for (var i = 0; i < tmp.length; ++i) {
        var result = tmp[i].split(',')
        var md = {};
        for (var j = 0; j < result.length; j++) {
            var txt = result[j];
            md[obj_format[j]] = txt;
        }
        rank_now[i] = md;
    }
    console.log(rank_now);

    var tmp = csv_data[1].split("\n");// 改行を区切り文字として行を要素とした配列を生成
    // 各行ごとにカンマで区切った文字列を要素とした二次元配列を生成
    for (var i = 0; i < tmp.length; ++i) {
        var result = tmp[i].split(',')
        var md = {};
        for (var j = 0; j < result.length; j++) {
            var txt = result[j];
            md[obj_format[j]] = txt;
        }
        rank_comp[result[3]] = md;
    }
    console.log(rank_comp);

    createTable();
}

function calc1() {

    var a1 = $('input[name="a1"]').val();
    var a2 = $('input[name="a2"]').val();
    var dt = new Date();
    dt.setFullYear(dt.getFullYear() - 1);
    var date_a1 = getNowYMDStr(a1);
    var date_a2 = getNowYMDStr(a2);
    // a2を空にするとa1の日付のランキングがみられる
    if(!a2){
        date_a2 = date_a1
    }
    // 1年以上前は取り出し禁止
    var dy = new Date(2021,10,20);
    var sn = $('select[name="world"]').val() ? Number($('select[name="world"]').val()) : 0;
    var jn = $('select[name="job"]').val() ? Number($('select[name="job"]').val()) : 0;

    var d1t = new Date(a1).getTime()
    var d2t = new Date(a2).getTime()
    var dtt = new Date(dt).getTime()
    var dyt = new Date(dy).getTime()
    if(d1t < dtt || d2t < dtt){
        alert("日付が古すぎます");
        return;
    } else if(d1t < dyt || d2t < dyt){
        if(jn != 0){
            alert("指定された日付の各職ランキングは取り出し不可");
            return;
        }
    }


    if(date_a1 && date_a2){
        getCSV(date_a1, date_a2,sn, jn);
    } else {
        alert("日付入力フォーマットエラー");
    }
}


function createTable() {
    var $div_main = $('<div>');
    var cnt = 0; //セーフティをはっておく

    var $table = $('<table>').attr("id", "table14").css("text-align", "center")
        .append($("<colgroup>").append($("<col>").attr("span", 1).attr("width", 80))
                                .append($("<col>").attr("span", 1).attr("width", 120))
                                .append($("<col>").attr("span", 1).attr("width", 200))
                                .append($("<col>").attr("span", 1).attr("width", 120))
                                .append($("<col>").attr("span", 1).attr("width", 80))
                                .append($("<col>").attr("span", 1).attr("width", 200))
                                );

    var $th_info = $('<tr>');
    var quest_title = "<th>順位</th><th>職業</th><th>名前</th><th>レベル</th><th>転生</th><th>差分</th>"
    $th_info.append(quest_title);
    $table.append($th_info);

    for (var i in rank_now) {
        if (cnt >= 2000) {
            console.log("2000件以上はhtml重くて出せないよ");
            break;
        }
        var data = rank_now[i];
        if(!data["rank"] || !data["name"]){
            continue;
        }
        var comp_data = rank_comp[data["name"]];
        var diff = "";
        if(comp_data){
            var diff_lv = Number(data.lv) - Number(comp_data.lv);
            if(diff_lv > 0){
                diff = '<font color="red">+'+diff_lv+'Lv</font>';
            } else if (diff_lv < 0){
                diff = '<font color="blue">-'+diff_lv+'Lv</font>';
            } else {
                diff = '<font color="blue">-</font>';
            }
        } else {
            // 新規登録？
            diff = '<font color="red">新規</font>';
        }

        var $rp = $('<tr>');//{0: "rank", 1: "img",2: "job", 3:"name", 4:"lv", 5:"returner"};
        var user_data = "<td>"+ data["rank"] +"</td><td>"+ data["job"] +"</td><td>"+data["name"]+"</td><td>"+data["lv"]+"</td><td>"+data["returner"]+"</td><td>"+diff+"</td>";
        $rp.append(user_data);
        $table.append($rp);
        cnt++;
    }

    $div_main.append($table);
    $div_main.append("<br><br>");

    $("#preview_html").empty().append($div_main);

}

