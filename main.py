from threading import Thread

import gi

import sys
import asyncio
import websockets

# gi.require_version('GstRtspServer', '1.0')
# gi.require_version('GstApp', '1.0')

# gi.require_version('GstVideo', '1.0')


gi.require_version("Gst", "1.0")
gi.require_version("GstApp", "1.0")
# gi.require_version('Gtk', '3.0')

from gi.repository import Gst, GLib, GstApp

Gst.init(None)
main_loop = GLib.MainLoop()
thread = Thread(target=main_loop.run)
thread.start()

path = "test.wav"
#command = "filesrc location=" + path + " ! decodebin ! audioconvert !  appsink name=audio"
command = "filesrc  location= video.sdp ! sdpdemux ! queue ! decodebin ! audioconvert !  appsink name=audio"


pipeline = Gst.parse_launch(command)
pipeline.set_state(Gst.State.PLAYING)

appsink = pipeline.get_by_name("audio")

uri = "ws://localhost:8888/kurento"
# sample = appsink.try_pull_sample(Gst.SECOND)
# print(sample)


async def run_test(uri):
    async with websockets.connect(uri) as websock:
        # wf = open(sys.argv[1], "rb")
        while True:

            # data = wf.read(8000)
            sample = appsink.try_pull_sample(Gst.SECOND)

            if sample is None:
                continue

            buffer = sample.get_buffer()

            (result, mapinfo) = buffer.map(Gst.MapFlags.READ)

            data = mapinfo.data

            await websock.send(data)
            print(await websock.recv())
            
            

        await websocket.send('{"eof" : 1}')
        print(await websocket.recv())
	
        PORT = '8888'
	
        async def echo(websocket, path):
            print("A client just connected")
            try:
                async for message in websocket:
                   await websocket.send(await websock.recv())
            except websockets.exceptions.ConnectionClosed as e:
                print("A client just disconnected")

        start_server = websockets.serve(echo, "0.0.0.0", PORT)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

# server 'ws://212.3.126.104:8053'

asyncio.get_event_loop().run_until_complete(
    run_test('ws://194.233.160.173:8053'))

