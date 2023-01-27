from flask import Flask, request, send_file
from flask_cors import CORS
import package.xml2geojson
import xmltodict
import os
import time
import random
import shutil

app = Flask(__name__)
CORS(app)

def gen_tmp_directory():
  rn = random.randint(0, 199)
  unix_time = int(time.time())
  dir_name = str(unix_time) + str(rn)
  path = './tmp/' + dir_name
  os.mkdir(path)
  return dir_name
  

@app.route("/mojxml2geojson", methods=['POST'])
def conv_mojxml_to_geojson():

  # 一時ディレクトリ生成
  dir_name = gen_tmp_directory()

  try:
    # ファイル数分処理する
    for key, file in request.files.items():
      # POSTされたデータ
      mojxml_data = file
      # データのファイル名
      file_name = file.filename

      # requestデータをパースしてstrに変換
      moj_dict = xmltodict.parse(mojxml_data)

      # 文字列化した地図XMLをGeojsonに変換
      package.xml2geojson.conv_mojxml_to_geojson(moj_dict, False, file_name, dir_name)

    new_archibe_path = shutil.make_archive(dir_name, 'zip', root_dir='./tmp/' + dir_name)
    shutil.rmtree('./tmp/' + dir_name)
    new_path = shutil.move(new_archibe_path, './dist_tmp')

    download_file = new_path
    MIMETYPE = 'application/octet-stream'
    return send_file(download_file, as_attachment=True,
                      download_name=file_name,
                      mimetype=MIMETYPE)
  except Exception:
    print('error')
    return 'Error Source File:'

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port='8888')