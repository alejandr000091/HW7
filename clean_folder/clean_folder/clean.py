import sys
from pathlib import Path
import os
import stat
import shutil



CATEGORIES = {"Audio": [".mp3", ".wav", ".flac", ".wma", ".ogg", ".wav", ".amr"],
              "Docs": [".docx", ".txt", ".pdf", ".doc", ".xlsx", ".pptx"],
              "Img": [".jpeg", ".png", ".jpg", ".svg", ".tif"],
              "Movie": [".avi", ".mp4", ".mov", ".mkv"],
              "Archive": [".zip", ".gz", ".tar"]}

TRANS = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G',
        1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 
        1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 
        1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 
        1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 
        1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 
        1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 
        1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e', 1069: 'E', 1102: 'yu', 
        1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 
        1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'}

def normalize(name):
    result_name = name.translate(TRANS)
    trans_name = ""
    for ch in result_name:
        if 48 <= ord(ch) <= 57 or 65 <= ord(ch) <= 90 or 97 <= ord(ch) <= 122:
            trans_name += ch
        else:
            trans_name += "_"
    return trans_name

def get_categories(file:Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def move_file(file:Path, category:str, root_dir:Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    new_path = target_dir.joinpath(file.name)
    if not new_path.exists():
        file.replace(new_path)
    else:
        file.replace(new_path)

def rm_dir_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)

def remove_empty_dir(element):
    try:
        if not any(os.scandir(element)):
            shutil.rmtree(element, onerror=rm_dir_readonly)
        else:
            print(f"{element} folder is not empty and could not be removed.")
    except OSError as e:
        print(f"Error: {e}")


def create_file_list(file_lst):
    audio_files_lst = ["AUDIO FILES FOUND", ]
    docs_files_lst = ["DOCS FILES FOUND", ]
    img_files_lst = ["IMG FILES FOUND"]
    movie_files_lst = ["MOVIE FILES FOUND"]
    archive_files_lst = ["ARCHIVE FILES FOUND",]
    other_files_lst = ["OTHER FILES FOUND",]
    knew_ex = ["KNEW EX", ]
    other_ex = ["OTHER(UNKNOWN) EX", ]
    for i in file_lst:
        category = i.split("---")[0]
        element = i.split("---")[1]
        ex = i.split("----")[1]
        for cat, exs in CATEGORIES.items():
            if ex in exs:
                if ex not in knew_ex:
                    knew_ex.append(ex)
        if category == "Other":
            if ex not in other_ex:
                other_ex.append(ex)

        if category == "Audio":
            audio_files_lst.append(element)
        elif category == "Docs":
            docs_files_lst.append(element )
        elif category == "Img":
            img_files_lst.append(element)
        elif category == "Movie":
            movie_files_lst.append(element)
        elif category == "Archive":
            archive_files_lst.append(element)
        elif category == "Other":
            other_files_lst.append(element)
    RESULT_TO_WRITE = ""
    for el in audio_files_lst:
        RESULT_TO_WRITE += el + "\n"
    for el in docs_files_lst:
        RESULT_TO_WRITE += el + "\n"
    for el in img_files_lst:
        RESULT_TO_WRITE += el + "\n"
    for el in movie_files_lst:
        RESULT_TO_WRITE += el + "\n"
    for el in archive_files_lst:
        RESULT_TO_WRITE += el + "\n"
    for el in other_files_lst:
        RESULT_TO_WRITE += el + "\n"
    for el in knew_ex:
        RESULT_TO_WRITE += el + "\n"
    for el in other_ex:
        RESULT_TO_WRITE += el + "\n"   
    return RESULT_TO_WRITE #audio_files_lst, docs_files_lst, img_files_lst, movie_files_lst, archive_files_lst, other_files_lst, knew_ex, other_ex

def sort_folder(path:Path) -> None:
    file_lst = []
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            result_el = "".join(category + "---" + str(element.name) + "----" + str(element.suffix))
            file_lst.append(result_el)
    write_result_str = create_file_list(file_lst)


    min_depth = 0
    max_depth = 0
    for element in path.glob("**/*"):
        current_len = len(str(element).split("\\"))
        if current_len > max_depth:
            max_depth = current_len
            if min_depth == 0:
                min_depth = max_depth
        elif current_len < min_depth:
            min_depth = current_len

        normalized_name = ""
        withou_ex_name = ""
        if element.is_file():
            withou_ex_name = element.name.split(".")
            normalized_name = normalize(withou_ex_name[0]) +"." + withou_ex_name[1]
            #print(normalized_name)
            if normalized_name != element.name:
                element.replace(element.parent.joinpath(normalized_name))
    folder_depth = max_depth - min_depth


    for element in path.glob("**/*"):
        if element.is_dir():
            if element.name in ("Audio", "Docs", "Img", "Movie", "Archive", "Other"):
                continue
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
    i = 0
    while i < folder_depth:
        for element in path.glob("**/*"):  
            if element.name in ("Audio", "Docs", "Img", "Movie", "Archive", "Other"):
                continue    
            if element.is_dir():
                remove_empty_dir(element)
        i += 1


    #unpack_zip def
    for arc in path.joinpath("Archive").iterdir():
    # if not arc.is_dir:
        archive_folder_name = arc.name.split(".")[0]
        new_path = path.joinpath("Archive").joinpath(archive_folder_name)
        shutil.unpack_archive(arc, new_path)
    
    path_to_write_file = path.joinpath("Docs").joinpath("result_execution.txt")
    with open(path_to_write_file, 'w+') as fh:
        fh.write(write_result_str) 

# def main() -> str:
def main_sort() -> str:
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return "Folder dos not exists"
    
    sort_folder(path)
    
    return "All Ok"


if __name__ == '__main__':
    print(main_sort())
    #main()