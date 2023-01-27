# coding: utf-8

import os
import xmltodict
import package.MojXmlDef as MojXmlDef
import package.MojXmlPolygon as MojXmlPolygon
import package.MojXMLtoGeoJSON as MojXMLtoGeoJSON

# 法務局地図XMLをGeojson形式に変換する関数
def conv_mojxml_to_geojson(src_file, exclude_flag, file_name, dir_name):

    # 地図XMLをオブジェクトに変換
    moj_obj = mojxml_to_obj(src_file)

    # 地図オブジェクトをJsonに変換
    mojGeojson = MojGeojson(moj_obj, exclude_flag)

    # JSONをファイル出力
    # path = os.path.dirname(src_file)
    name = os.path.splitext(os.path.basename(file_name))[0]

    save_name = name + ".geojson"
    path = './tmp/' + dir_name
    dst_name = path + '/' + save_name

    with open(dst_name, 'w', encoding='utf-8') as f:
        f.write(mojGeojson)
        f.close()


# 地図XMLをオブジェクトに変換する関数
def mojxml_to_obj(src_file):

    # 地図XMLをオブジェクトとして読み込む
    # with open(src_file, encoding='utf-8') as fp:
    #     xml_data = fp.read()
    # moj_dict = xmltodict.parse(src_file)

    moj_dict = src_file
    # 地図XMLのプロパティを取得
    version = moj_dict['地図']['version']
    map_name = moj_dict['地図']['地図名']
    city_code = moj_dict['地図']['市区町村コード']
    city_name = moj_dict['地図']['市区町村名']
    crs = moj_dict['地図']['座標系']
    # 測地系判別は存在しないかもしれないので、なかった場合にエラーを吐かないようgetで取得
    datum_type = moj_dict.get('地図', {}).get('測地系判別')

    # 座標系参照番号を取得
    number_crs, named_crs = MojXmlDef.GetCrs(crs)

    # ポリゴンを取得
    mojXmlPolygon = MojXmlPolygon.MojXmlPolygon(moj_dict)

    mojObj = {
        'version': version,
        'map_name': map_name,
        'city_code': city_code,
        'city_name': city_name,
        'crs': crs,
        'named_crs': named_crs,
        'number_crs': number_crs,
        'datum_type': datum_type,
        'mojXmlPolygon': mojXmlPolygon,
    }
    return mojObj


def MojGeojson(mojObj: dict, exclude_flag):
    return MojXMLtoGeoJSON.MojXMLtoGeoJSON(mojObj, exclude_flag)
