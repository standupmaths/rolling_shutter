from PIL import Image
import glob
import ffmpy
import sys
import tempfile
import shutil

def extract_frames(vid,folder):
    print('extracting frames')
    ff=ffmpy.FFmpeg(inputs={str(vid):None},outputs={str(folder)+'/frame%05d.png':'-loglevel panic'})
    ff.run()

def compose_vid(folder,vid):
    print('composing video')
    ff=ffmpy.FFmpeg(inputs={str(folder)+'/frame%05d.png':None},outputs={str(vid):'-loglevel panic'})
    ff.run()
    print('output video ' + str(vid) + ' written')

def rs(in_folder,out_folder,speed=1):
    print('applying rolling shutter effect')
    
    #get frame dimensions
    frame1=Image.open(str(in_folder)+'/frame00001.png')
    width,height = frame1.size
    frame1.close()

    count=len(glob.glob(str(in_folder)+'/frame?????.png'))

    beg=1
    end=height//speed

    frames=[Image.open(str(in_folder)+('/frame%05d.png' % i)) for i in range(beg,end+1)]
    
    while(end<=count):
        # Making our blank output frame
        output_image = Image.new('RGB', (width, height)) 
        
        # let us go through the frames one at a time
        
        current_row = 0
        
        for i in frames:
            new_line = i.crop((0, current_row, width, current_row+speed))
            output_image.paste(new_line, (0,current_row))
            current_row += speed

        # and export the final frame
        output_image.save(str(out_folder) + ('/frame%05d.png' % beg))

        beg+=1
        end+=1
        frames[0].close()
        frames.pop(0)
        frames.append(Image.open(str(in_folder)+('/frame%05d.png' % end)))
        
    

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("please specify input video")
        sys.exit(1)
    tmp_in=tempfile.mkdtemp(suffix='in')
    tmp_out=tempfile.mkdtemp(suffix='out')
    vid_in=sys.argv[1]
    vid_out=vid_in.split('.')
    if len(vid_out) == 1:
        vid_out='.'.join(vid_out) + '_out'
    else:
        vid_out='.'.join(vid_out[:-1])+'_out.'+vid_out[-1]
    try:
        extract_frames(vid_in,tmp_in)
    except:
        print('extraction failed')
        count=len(glob.glob(str(tmp_in)+'/frame?????.png'))
        print('only %d  got frames' % count)
    try:
        rs(tmp_in,tmp_out,1)
    except:
        print('shutter effect failed')
    try:
        compose_vid(tmp_out,vid_out)
    except:
        print('composing video from frames failed')
    shutil.rmtree(tmp_in)
    shutil.rmtree(tmp_out)
    print('Done.')

