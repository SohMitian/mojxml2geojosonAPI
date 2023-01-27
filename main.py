import traceback
import package.xml2geojson

def main():
    srcFile = '13101-0100-1.xml'
    try:
        package.xml2geojson.conv_mojxml_to_geojson(srcFile, False)
    except Exception:
        print('Error Source File:', srcFile)
        traceback.print_exc()


if __name__ == '__main__':
    main()
