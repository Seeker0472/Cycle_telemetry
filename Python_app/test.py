from Service import mp4_gpx_extractor, fitphaser, fit
from db import read_data

# fitphaser.phase_fit("C:\\Users\\gmx47\\OneDrive\\桌面\\test\\te.fit", "TestFit")
#
# mp4_gpx_extractor.extract_mp4("C:\\Data\\100GOPRO\\GH030107.MP4", "testMp4")
#
# mp4_gpx_extractor.read_gpx('C:\\Data\\AAExample\\route1.gpx', "TestGpx")
#
# print(mp4_gpx_extractor.get_mp4_start_end("C:\\Data\\100GOPRO\\GH030107.MP4"))

da = fit.create_fit("TABLE_0")
print(da)
