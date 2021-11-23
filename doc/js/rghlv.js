const server_name = ["strasserad", "vaultish", "bridgehead"];

//CSVファイルを読み込む
function getCSV(date1, date2, server) {
    url1 = "https://sokomin.github.io/RS-Ranking/out/jpn_gh/" + date1 + "_" + server_name[server] + "_1.csv";
    url2 = "https://sokomin.github.io/RS-Ranking/out/jpn_gh/" + date1 + "_" + server_name[server] + "_3.csv";
    url3 = "https://sokomin.github.io/RS-Ranking/out/jpn_gh/" + date1 + "_" + server_name[0] + "_5.csv";
    url4 = "https://sokomin.github.io/RS-Ranking/out/jpn_gh/" + date2 + "_" + server_name[server] + "_1.csv";
    url5 = "https://sokomin.github.io/RS-Ranking/out/jpn_gh/" + date2 + "_" + server_name[server] + "_3.csv";
    url6 = "https://sokomin.github.io/RS-Ranking/out/jpn_gh/" + date2 + "_" + server_name[0] + "_5.csv";

    var request = [
        { url: url1 },
        { url: url2 },
        { url: url3 },
        { url: url4 },
        { url: url5 },
        { url: url6 },
    ];

    var jqXHRList = [];

    for (var i = 0; i < request.length; i++) {
        jqXHRList.push($.ajax({
            url: request[i].url,
            type: 'GET',
        }));
    }

    $.when.apply($, jqXHRList).done(function () {
        var csv_data = [];
        var statuses = [];
        var jqXHRResultList = [];
        for (var i = 0; i < arguments.length; i++) {
            var result = arguments[i];
            csv_data.push(result[0]);
            statuses.push(result[1]);
            jqXHRResultList.push(result[3]);
        }

        console.log(csv_data);
        convertCSVtoArray(csv_data, server);

    });
}

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
}

var obj_format = { 0: "rank", 1: "img", 2: "guild_name", 3: "gm_name", 4: "pwar_pt", 5: "gh_rank" };
var rank_now = {};
var rank_comp = {};

function convertCSVtoArray(csv_data, sn) {
    // 初期化
    rank_now = {};
    rank_comp = {};

    /**
     * now側
     */
    var result = [];
    var tmp1 = csv_data[0].split("\n");
    var tmp3 = csv_data[1].split("\n");
    var tmp5 = csv_data[2].split("\n");

    // Rank5
    for (var i = 0; i < tmp5.length; ++i) {
        var result = tmp5[i].split(',')
        var md = {};
        for (var j = 0; j < result.length; j++) {
            var txt = result[j];
            md[obj_format[j]] = txt;
        }
        // 一致するサーバのデータだけ取得
        if (sn == i) {
            md.gh_rank = 5;
            rank_now[0] = md;
            break;
        }
    }

    // Rank3と4
    var cnt = 0;
    for (var i = 1; i < tmp3.length; ++i) {
        var result = tmp3[i - 1].split(',')
        var md = {};
        // 最初の3行がGH Rank4なのでrank4
        for (var j = 0; j < result.length; j++) {
            var txt = result[j];
            md[obj_format[j]] = txt;
        }
        if (cnt < 3) {
            md.gh_rank = 4;
        } else {
            md.gh_rank = 3;
        }
        cnt++;
        rank_now[i] = md;
    }
    // Rank2と1
    cnt = 0;
    for (var i = tmp3.length; i < (tmp3.length + tmp1.length - 1); ++i) {
        var result = tmp1[i - tmp3.length].split(',')
        var md = {};
        // 最初の27行がGH Rank2なのでrank2
        for (var j = 0; j < result.length; j++) {
            var txt = result[j];
            md[obj_format[j]] = txt;
        }
        if (cnt < 27) {
            md.gh_rank = 2;
        } else {
            md.gh_rank = 1;
        }
        cnt++;
        rank_now[i] = md;
    }
    console.log(rank_now);

    /**
     * comp側
     */
    var result = [];
    var tmp1 = csv_data[3].split("\n");
    var tmp3 = csv_data[4].split("\n");
    var tmp5 = csv_data[5].split("\n");

    // Rank5
    for (var i = 0; i < tmp5.length; ++i) {
        var result = tmp5[i].split(',')
        var md = {};
        for (var j = 0; j < result.length; j++) {
            var txt = result[j];
            md[obj_format[j]] = txt;
        }
        // 一致するサーバのデータだけ取得
        if (sn == i) {
            md.gh_rank = 5;
            rank_comp[result[2]] = md;
            break;
        }
    }

    // Rank3と4
    var cnt = 0;
    for (var i = 1; i < tmp3.length; ++i) {
        var result = tmp3[i - 1].split(',')
        var md = {};
        // 最初の3行がGH Rank4なのでrank4
        for (var j = 0; j < result.length; j++) {
            var txt = result[j];
            md[obj_format[j]] = txt;
        }
        if (cnt < 3) {
            md.gh_rank = 4;
        } else {
            md.gh_rank = 3;
        }
        cnt++;
        rank_comp[result[2]] = md;
    }
    // Rank2と1
    cnt = 0;
    for (var i = tmp3.length; i < (tmp3.length + tmp1.length - 1); ++i) {
        var result = tmp1[i - tmp3.length].split(',')
        var md = {};
        // 最初の27行がGH Rank2なのでrank2
        for (var j = 0; j < result.length; j++) {
            var txt = result[j];
            md[obj_format[j]] = txt;
        }
        if (cnt < 27) {
            md.gh_rank = 2;
        } else {
            md.gh_rank = 1;
        }
        cnt++;
        rank_comp[result[2]] = md;
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
    if (!a2) {
        date_a2 = date_a1
    }
    // 1年以上前は取り出し禁止
    var dy = new Date(2021, 10, 20);
    var sn = $('select[name="world"]').val() ? Number($('select[name="world"]').val()) : 0;

    var d1t = new Date(a1).getTime()
    var d2t = new Date(a2).getTime()
    var dtt = new Date(dt).getTime()
    var dyt = new Date(dy).getTime()
    if (d1t < dtt || d2t < dtt) {
        alert("日付が古すぎます");
        return;
    } else if (d1t < dyt || d2t < dyt) {
        alert("指定された日付のランキングは取り出し不可");
        return;
    }


    if (date_a1 && date_a2) {
        getCSV(date_a1, date_a2, sn);
    } else {
        alert("日付入力フォーマットエラー");
    }
}


function createTable() {
    var $div_main = $('<div>');
    var cnt = 0; //セーフティをはっておく
    var pwar_ptsum = 0;
    var pwar_ptcnt = 0;

    var $table = $('<table>').attr("id", "table14").css("text-align", "center")
        .append($("<colgroup>").append($("<col>").attr("span", 1).attr("width", 80))
            .append($("<col>").attr("span", 1).attr("width", 80))
            .append($("<col>").attr("span", 1).attr("width", 200))
            .append($("<col>").attr("span", 1).attr("width", 200))
            .append($("<col>").attr("span", 1).attr("width", 200))
            .append($("<col>").attr("span", 1).attr("width", 200))
        );

    var $th_info = $('<tr>');
    var quest_title = "<th>ランク</th><th>順位</th><th>ギルド名</th><th>ギルドマスター</th><th>P戦ポイント</th><th>差分</th>"
    $th_info.append(quest_title);
    $table.append($th_info);

    for (var i in rank_now) {
        if (cnt >= 2000) {
            console.log("2000件以上はhtml重くて出せないよ");
            break;
        }
        var data = rank_now[i];
        if (!data["rank"] || !data["guild_name"]) {
            continue;
        }
        var comp_data = rank_comp[data["guild_name"]];
        var diff = "";
        if (comp_data) {
            var diff_pt = Number(data.pwar_pt) - Number(comp_data.pwar_pt);
            if (diff_pt > 0) {
                diff += ' <font color="gray">P戦更新</font>';
            }
            var diff_rank = Number(data.gh_rank) - Number(comp_data.gh_rank);
            if (diff_rank > 0) {
                diff += ' <font color="red">Rank↑</font>';
            } else if (diff_rank < 0){
                diff += ' <font color="blue">Rank↓</font>';
            }
        } else {
            // 新規ギルドとして扱う
            diff += ' <font color="red">新規</font>';
        }
        // 集計用
        if(data.pwar_pt > 9645000){
            pwar_ptsum+= Number(data.pwar_pt);
            pwar_ptcnt++;
        }

        var $rp = $('<tr>');//{ 0: "rank", 1: "img", 2: "guild_name", 3: "gm_name", 4: "pwar_pt", 5: "gh_rank" };
        var user_data = "<td>" + data["gh_rank"] + "</td><td>" + data["rank"] + "</td><td>" + data["guild_name"] + "</td><td>" + data["gm_name"] + "</td><td>" + data["pwar_pt"] + "</td><td>" + diff + "</td>";
        $rp.append(user_data);
        $table.append($rp);
        cnt++;
    }

    var average_pt = pwar_ptcnt > 0 ? parseInt(pwar_ptsum / pwar_ptcnt) : "データ無し";
    $div_main.append("完遂時の平均P戦ポイント：" + average_pt + "<br><br>");
    $div_main.append($table);
    $div_main.append("<br><br>");

    $("#preview_html").empty().append($div_main);

}

