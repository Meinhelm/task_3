
import click
import eyed3
import os
import shutil

@click.command()
@click.option('-s', '--src-dir', default='.', help='Source directory.', show_default=True)
@click.option('-d', '--dst-dir', default='.', help='Destination directory.', show_default=True)
def music_sorter(src_dir, dst_dir):
    """Сортировка музыки"""
    while True:
        if os.path.isdir(src_dir):
            try:

                it = os.scandir(src_dir)
            except PermissionError as e:
                print(str(e))
                print('Введите путь до другой директории.Введите e для выхода')
                src_dir = input()
                if src_dir == 'e':
                    break
            else:
                with it:
                    for entry in it:
                        if not entry.name.startswith('.') and entry.is_file() \
                                and entry.name.lower().endswith('.mp3'):
                            try:
                                audiofile = eyed3.load(entry)
                                if not audiofile.tag.title:
                                    title = entry.name
                                else:
                                    title = audiofile.tag.title.replace('/', ':')
                                if not audiofile.tag.artist or not audiofile.tag.album:
                                    print(f'Недостаточно тегов для сортировки: {entry.name}')
                                    continue
                                else:
                                    artist = audiofile.tag.artist.replace('/', ':')
                                    album = audiofile.tag.album.replace('/', ':')
                                audiofile.tag.save()
                            except AttributeError as e:
                                print(f'Что-то не так с файлом: {entry.name}')
                            except PermissionError as e:
                                print(f'Недостаточно прав: {entry.name}')
                                continue
                            else:
                                new_file_name = f'{title} - {artist} - {album}.mp3'
                                if os.path.exists(os.path.join(dst_dir, artist, album)):
                                    shutil.move(os.path.join(src_dir, entry.name),
                                                os.path.join(dst_dir, artist, album, new_file_name))

                                else:
                                    try:
                                        os.makedirs(os.path.join(dst_dir, artist, album))
                                    except PermissionError as e:
                                        print(str(e))
                                        print('Введите путь до другой директории. Введите e для выхода.')
                                        dst_dir = input()
                                        if dst_dir == 'e':
                                            break
                                    else:
                                        shutil.move(os.path.join(src_dir, entry.name),
                                                    os.path.join(dst_dir, artist, album, new_file_name))
                                print(f'{os.path.join(src_dir, entry.name)} '
                                      f'-> {os.path.join(dst_dir, artist, album, new_file_name)}')
                print('Все работает.')
                break
        else:
            print('Директория не найдена.')
            print('Введите путь в существующий каталог. Введите e для выхода.')
            src_dir = input()
            if src_dir == 'e':
                break


if __name__ == '__main__':
    music_sorter()