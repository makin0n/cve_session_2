FILES = \
	libretro-common/formats/cdfs/cdfs.c \
	libretro-common/streams/file_stream.c \
	libretro-common/streams/file_stream_transforms.c \
	libretro-common/streams/interface_stream.c \
	libretro-common/streams/memory_stream.c \
	libretro-common/vfs/vfs_implementation.c \
	libretro-common/compat/compat_strl.c \
	libretro-common/file/file_path.c \
	libretro-common/file/file_path_io.c \
	libretro-common/string/stdstring.c \
	libretro-common/time/rtime.c \
	libretro-common/encodings/encoding_utf.c \
	libretro-common/encodings/encoding_crc32.c

exploit: exploit.c $(FILES)
	gcc -Ilibretro-common/include exploit.c $(FILES) -o exploit

run: exploit
	./exploit overflow.cue

