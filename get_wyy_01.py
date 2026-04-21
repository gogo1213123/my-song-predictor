import requests
import time
from datetime import datetime
import pandas as pd
import os
import csv
import re

# ========== 配置区域 ==========
PLAYLIST_ID = 761345092     # 你的网易云歌单ID
COOKIE = "_ga=GA1.1.774330968.1754272199; _ga_EPDQHDTJH5=GS2.1.s1754272198$o1$g0$t1754272203$j55$l0$h0; nts_mail_user=18213157611@163.com:-1:1; NTES_P_UTID=khu4igqd5VW43PLK9puD6TL8IHiGIQSX|1775787726; NTES_PASSPORT=aAQFp5xzIhbUcxeKarvmobj7FbtLHwR8Y5MIpnaWJG.QHglxHydKU4hTPlYuHgzCv8xs_DvUfV4ZyXYa.yP.rxs6GCCCOHZE11U1RFJ7HBXezcxVvhAXqN_TF5nD2r6LZpfgz4e1QWT4CHRcCiHP.bAuBuY9XbxvN2nVznRNIWxbw55HZu_hn4N0ouFB31yZi; P_INFO=m18213157611@163.com|1775787726|1|mail163|00&99|null&null&null#gud&440100#10#0#0|182611&1|mail163|18213157611@163.com; JSESSIONID-WYYY=7JQcQS%2BoG8JYyZm6A50FtrFZ55dbuUi7lN9ivvbI1Fty%2F1zi9nbK%2FqxuSD8Tb5aQlPjC0CBomFI4eZnzjT2NbjRpH%5CzsxZHkjfEbs8GfMCfbHdjtaZUs7MSIb2y8uYQ6Cv8habnR5qurEalp0gUZ2m%2FvBDGbVNq5E7Wa1eOf9zwETIKt%3A1776668685964; _iuqxldmzr_=32; _ntes_nnid=f6a17087dd14b4f84c9c56072a57c6ab,1776666886017; _ntes_nuid=f6a17087dd14b4f84c9c56072a57c6ab; NMTID=00OW-rIkp8mNriwNEeRrFcmYbbsE3gAAAGdqZktWA; Hm_lvt_1483fb4774c02a30ffa6f0e2945e9b70=1776666887; HMACCOUNT=F72D084F1E68C984; WEVNSM=1.0.0; WNMCID=yczbkf.1776666896428.01.0; sDeviceId=YD-QSTL4QSnTS1EAwBFFBLHstyTgsfGbMqT; WM_NI=Ucxjpl%2BMuPELfanBWOc8GDbV%2FQGhUV1TOhAU9kL2KyI5StRQbQdQGgh%2FQOMmcfynCUxtdaTOi51jxiE2UTffvM0Rwhpty8soE9xVeSsCj6BwYj9jWZip80yR4rO22TLIWmI%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee89aa5faf978997d04ff8b48ab3c44e978e9f87c634fced9cd1f76b9ab8aeb9d52af0fea7c3b92a97bdb88bf368e993bbb1c848a6bfa2a3d645a1e889a5e15eed8f8989d85ef38c8189c45ffbb584d3ca738beb9d95d15ba28facb2c66dacf19fb0d067a1bab78fc25fbcacac82d745abebff8bfb6387ee9bb5e56eb69300b3f664b4acb7d9f26587e7b8b7e859b19da6d7c17d9bb6f78bd652abb0f8d1fc5af8ae81d3b1609097998ecc37e2a3; WM_TID=hfXkWqQViJxAARRVRQfXp5iGgtaZlKHB; __snaker__id=A9ALNCqMvUBL4y4U; ntes_utid=tid._.yLSbqnq%252BDQhAEgFUARPS542C0thM1t9H._.0; gdxidpyhxdE=Cln%2F1Tl2U36ZQT4z3yPfDlC5Izhn9Y6LkqryWYX%2BRzvmOfekQr4OsUYmnDwvT0CLpX47BewC%2BEcRzLK%2FDnZn3%5CuzgPA7Ub3YuohmmIJQfTx4oOUVd9Y5VZxavukiCVagMJZZ%2F7IWhKALj6JLTr59ukkHtvHXKUCUqapsjBalzuDgfZVk%3A1776667853109; __csrf=b5d7ad212ea7a55b69215c23be43f2d8; MUSIC_U=0079C4DBA1DD9411642EF233967BB8BD07285BDA47C61D865982467115D2CCD977E3F53E6538D7A053BEA72306586C25012588B7A63671EA8FFB4D02DF4459DAA43997FFCE6A380C0F4846B2B533E72A270C46F0D4D5E56419C03D9D3122A56AA5918429DE1E68ED42C7FBD0F04525530D8582AD63EF18A863EE43DE3114E96ADEC79445984AB289518E67A9BA3D6DE3E8A0AEF3182DEE216A9C53525F5A0FF0C76BA057EE6CA5396EC1C4659ABF0EBB055215928EE81BCF21DE4D0A51F2E33FDFB0A036639F73A8B4175E4BB938803B2C1467976E2D1AAE9721AB0DBB7B2B1EDB2B8513525540A4BE730F87E3C31F55701503AA42BB1F0711910F744A13D58249701ED72B81E81B232EB18307BEC67C6C44BA534DFBB607FAAF8F70F7152F96C71B0118C5349798C638122E69DA88FFD5B2E5F4CF39CB87386E8080890090AD62C2B730F1769CC2955FAE505A5078180197F75893D29233067D585FF61D5B3AAF3BFE3BCDE6B04C6E0B285791DC46D0683630C5AAC3E42C47946828855C0F4EF04EE36310097676EAB517DE90D0A8F307AE09D2D8F388A2D5BFD202E0F3289940; ntes_kaola_ad=1; Hm_lpvt_1483fb4774c02a30ffa6f0e2945e9b70=1776667670"  # 完整Cookie字符串（从浏览器复制）
DEEPSEEK_API_KEY = "sk-e4537ccc4a8e4ae791e58435b48f921e"
BATCH_SIZE = 200                   # 每批分析的歌曲数（根据token限制调整）
API_BASE = "http://localhost:3000" # 本地网易云API服务地址
# ============================

def get_all_songs_from_playlist():
    """通过本地网易云API服务获取歌单中所有歌曲（分页自动获取全部）"""
    songs = []
    limit = 1000  # 每次请求最大数量
    offset = 0
    total = None

    while True:
        url = f"{API_BASE}/playlist/track/all"
        params = {
            "id": PLAYLIST_ID,
            "limit": limit,
            "offset": offset
        }
        headers = {"Cookie": COOKIE}
        try:
            resp = requests.get(url, params=params, headers=headers)
            data = resp.json()
            if data.get("code") != 200:
                print(f"接口错误: {data}")
                break
            # 提取歌曲列表
            tracks = data.get("songs", [])
            for track in tracks:
                name = track.get("name")
                artists = track.get("ar", [])
                artist = artists[0].get("name") if artists else "未知歌手"
                songs.append(f"{name} - {artist}")
            # 判断是否还有更多
            if total is None:
                total = data.get("total", 0)
                print(f"歌单共 {total} 首歌曲")
            offset += limit
            if offset >= total:
                break
            time.sleep(0.5)  # 避免请求过快
        except Exception as e:
            print(f"请求出错: {e}")
            break
    return songs

def analyze_batch(songs_batch, batch_index):
    """调用 DeepSeek 分析一批歌曲，返回分析文本"""
    prompt = f"""
请分析以下歌单的风格，并用一个词总结整体风格（只能从以下选择：流行、摇滚、电子、民谣、说唱、古典、爵士、其他）。输出格式：最后一行单独写“STYLE: 标签”。

这是第 {batch_index} 批分析。

歌单内容：
{chr(10).join(songs_batch)}
"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    resp = requests.post("https://api.deepseek.com/v1/chat/completions",
                         headers=headers, json=payload, timeout=60)
    result = resp.json()
    if "error" in result:
        raise Exception(f"API错误: {result['error']['message']}")
    return result["choices"][0]["message"]["content"].strip()

def extract_style_tag(analysis_text):
    """从分析文本中提取 STYLE: 标签后的内容"""
    match = re.search(r'STYLE:\s*(\S+)', analysis_text)
    if match:
        return match.group(1)
    return "未提取到标签"

def main():
    print("正在从网易云获取歌单...")
    all_songs = get_all_songs_from_playlist()
    if not all_songs:
        print("获取歌单失败，请检查歌单ID、Cookie以及本地API服务是否正常运行。")
        return

    total = len(all_songs)
    print(f"成功获取 {total} 首歌曲。")
    print("预览前10首：")
    for i, s in enumerate(all_songs[:10], 1):
        print(f"{i:2}. {s}")

    # 分批次
    batches = [all_songs[i:i+BATCH_SIZE] for i in range(0, total, BATCH_SIZE)]
    print(f"\n共分为 {len(batches)} 批，每批最多 {BATCH_SIZE} 首，开始调用 DeepSeek 分析...")

    records = []  # 存储每批次的字典记录
    stop_flag = False
    for idx, batch in enumerate(batches, 1):
        if stop_flag:
            break
        print(f"\n正在分析第 {idx}/{len(batches)} 批（{len(batch)} 首）...")
        record = {
            "batch_index": idx,
            "songs_count": len(batch),
            "songs_list": "；".join(batch),  # 用分号分隔歌曲
            "style_tag": "",
            "status": "success",
            "error_reason": "",
            "analysis_text": ""
        }
        try:
            analysis = analyze_batch(batch, idx)
            record["analysis_text"] = analysis
            record["style_tag"] = extract_style_tag(analysis)
            print(f"第 {idx} 批完成，风格标签：{record['style_tag']}")
            time.sleep(1)
        except Exception as e:
            error_msg = str(e)
            record["status"] = "failed"
            record["error_reason"] = error_msg
            if "context_length_exceeded" in error_msg or "maximum context length" in error_msg:
                print(f"⚠️ 第 {idx} 批因 token 超限失败，已停止后续分析。")
                stop_flag = True
            elif "Insufficient Balance" in error_msg or "402" in error_msg:
                print(f"⚠️ 余额不足，停止分析。")
                stop_flag = True
            else:
                print(f"❌ 第 {idx} 批分析出错: {error_msg}")
                # 其他错误继续尝试下一批
        records.append(record)

    # 写入 CSV 文件
    # 将每批次的歌曲拆成单独的行，追加到 songs.csv
    csv_accumulate = "songs.csv"  # 固定文件名
    file_exists = os.path.isfile(csv_accumulate)

    with open(csv_accumulate, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["song_name", "artist", "genre", "batch_index", "source_playlist_id"])

        for rec in records:
            if rec["status"] != "success":
                continue
            style_tag = rec["style_tag"]
            # 将 "歌名 - 歌手；歌名2 - 歌手2" 拆开
            songs_list = rec["songs_list"].split("；")
            for item in songs_list:
                if " - " in item:
                    name, artist = item.split(" - ", 1)
                else:
                    name, artist = item, "未知"
                writer.writerow([name, artist, style_tag, rec["batch_index"], PLAYLIST_ID])

    print(f"已追加到 {csv_accumulate}，累计歌曲数请用 pandas 查看。")

    # 输出汇总信息
    success_count = sum(1 for r in records if r["status"] == "success")
    print(f"\n✅ CSV 报告已生成: {csv_accumulate}")
    print(f"总批次数: {len(records)}，成功: {success_count}，失败: {len(records)-success_count}")
    if stop_flag:
        print("⚠️ 分析未完成，因 token 超限或余额不足而中断。请减小 BATCH_SIZE 后重新运行。")

if __name__ == "__main__":
    if DEEPSEEK_API_KEY == "" or not DEEPSEEK_API_KEY:
        print("❌ 请先配置有效的 DeepSeek API Key！")
        exit(1)
    if COOKIE == "MUSIC_U=0079C4D...; ..." or not COOKIE:
        print("❌ 请先配置你的网易云 Cookie！")
        exit(1)
    main()