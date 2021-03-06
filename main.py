from pytube import YouTube
import PyQt5.QtWidgets as qtw 
import PyQt5.QtGui as qtg
import ffmpeg, time
import moviepy.editor as mpe
import os, os.path
from notification import notif_download_started, notif_download_finished


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()


        #Set a title
        self.setWindowTitle("YouTube Downloader")

        #Set text
        self.setLayout(qtw.QVBoxLayout())
        #Create a label
        my_label = qtw.QLabel("Welcome to free to use YouTube Downloader")
        #Change the font size of label
        my_label.setFont(qtg.QFont('Helvetica', 18))
        self.layout().addWidget(my_label)
        
        #Set the url entry box
        my_entry = qtw.QLineEdit()
        my_entry.setObjectName("url_field")
        my_entry.setText("Paste youtube url here")
        self.layout().addWidget(my_entry)

       
        #Create a combo box
        my_combo = qtw.QComboBox(self)
        my_combo.addItem("144p", "144p")
        my_combo.addItem("240p", "240p")
        my_combo.addItem("360p", "360p")
        my_combo.addItem("480p", "480p")
        my_combo.addItem("720p", "720p")
        my_combo.addItem("1080p", "1080p")
        self.layout().addWidget(my_combo)

         #Create a combo box
        mp3_or_mp4 = qtw.QComboBox(self)
        mp3_or_mp4.addItem("mp4", "mp4")
        mp3_or_mp4.addItem("mp3", "mp3")
        self.layout().addWidget(mp3_or_mp4)

        #Create a button
        my_button = qtw.QPushButton("Download",
        clicked = lambda: press_it())
        self.layout().addWidget(my_button)

       
        
        #Show surf
        self.show()


        def press_it():

            #Keep data
            url = my_entry.text()
            quality = my_combo.currentText()
            vfound = False
            afound = False

            if url.find("youtube.com") != -1:

                #clear entry
                
                

                #Do pytube stuff
                my_entry.setText('Downloading...')
                print(url)
                print(quality)
                yt = YouTube(url)
                print(yt.title)


                videoVersions = yt.streams.filter(adaptive=True, mime_type="video/mp4")
                for version in videoVersions:
                    if version.resolution == quality:
                        vId = version.itag
                        vfound = True
                        print("Quality has been found among the ones available")
                audioVersions = yt.streams.filter(adaptive=True, audio_codec="mp4a.40.2")
                for version in audioVersions:
                    aId = version.itag
                    afound = True
                    print("Audio has been found")

                print(vId)
                print(aId)
                
                print(yt.streams.get_by_itag(vId).filesize)
                notif_download_started()
                if mp3_or_mp4.currentText == "mp4" :

                    if(afound and vfound):
                        yt.streams.get_by_itag(vId).download('./Downloads',filename="video")
                        yt.streams.get_by_itag(aId).download('./Downloads',filename="audio")
                    else:
                        yt.streams.first().download('./Downloads', filename="video")
                        yt.streams.get_by_itag(aId).download('./Downloads',filename="audio")


                    def combine_audio(vidname, audname, outname, fps=25):
                        my_clip = mpe.VideoFileClip(vidname)
                        audio_background = mpe.AudioFileClip(audname)
                        final_clip = my_clip.set_audio(audio_background)
                        final_clip.write_videofile(outname,fps=fps)
                    
                    combine_audio("./Downloads/video.mp4", "./Downloads/audio.mp4","./Downloads/" + yt.title + ".mp4")

                    os.remove("./Downloads/video.mp4")
                    os.remove("./Downloads/audio.mp4")
                    
                
                else:
                    yt.streams.get_by_itag(aId).download("./Downloads/")
                notif_download_finished()
            else:
                my_entry.setText("Please give a valid YouTube link")

app = qtw.QApplication([])
mw = MainWindow()

#Run the app
app.exec_()

