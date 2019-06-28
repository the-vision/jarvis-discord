import os

import discord
import youtube_dl as ytdl


class MusicPlayer:
    '''
        This module is responsible for connecting and disconnecting the bot from a voice channel, downloading songs from
        youtube and add them in the queue . Basic music functions like pause, resume, stop and play, in order to give
        users a simple music bot based on the new api of discord.
    '''

    def __init__(self):
        self.queue = []
        self.voiceChannel = None
        self.ydl_opts = {
            'format': 'bestaudio/best',
            # 'quiet' : True,
            'outtmpl': 'songs/%(title)s-%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',

            }],
        }

    async def connect(self, channel):
        '''
        Connects bot to the given voice channel. If it is not already connected.
        :param channel: The channel from which the user send the command
        '''
        if self.voiceChannel is None or not self.voiceChannel.is_connected():
            self.voiceChannel = await channel.connect()

    async def disconnect(self):
        '''
        Disconnects from the channel that the bot is already connected. If there is no such a channel,
        this function will simply do nothing
        '''
        if self.voiceChannel is not None and self.voiceChannel.is_connected():
            await self.voiceChannel.disconnect()

    def getNextSong(self):
        '''
        If the queue is not empty this function will remove the first song from the queue and return it
        :return: the next song of the queue, or None if the queue is empty
        '''
        if self.queue:
            return self.queue.pop(0)
        else:
            return None

    def clear_folder(self):
        '''
        Because the songs will be downloaded, it is important to delete them if there are not longer needed.
        This function deletes the songs that are not in the queue (not one of the upcoming songs)
        '''
        for song in os.listdir("songs/"):

            if "songs/" + song not in self.queue:
                os.remove("songs/" + song)

    async def add_song(self, url, ctx):
        '''
        Add a new song from the youtube in the queue. It will not be downloaded if it is already in the songs file
        :param url: The url of the youtube song
        :param ctx: The channel from which the user send the command
        '''
        with ytdl.YoutubeDL(self.ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = "songs/" + info_dict['title'] + "-" + info_dict['id'] + ".mp3"
            if title not in self.queue:
                await ctx.send("Your song is downloading now!")
                ydl.extract_info(url, download=True)
            self.queue.append(title)
        if self.voiceChannel is None or not self.voiceChannel.is_connected() or not self.voiceChannel.is_playing():
            await ctx.send("Your song has added to the queue, use $play to start the party!!")
        else:
            await ctx.send("Your song has added to the queue")

    def load_next_song(self):
        '''
        This will create a FFMPEG object and start playing it in the voice channel
        '''
        if not self.voiceChannel.is_playing() and self.queue:
            audio_source = discord.FFmpegPCMAudio(self.getNextSong())
            # TODO: make the bot play the next song after the previous one has ended
            self.voiceChannel.play(audio_source, after=None)

    async def pause_song(self, ctx):
        '''
        Pauses a song that is already being played or send a message if there is no such song
        :param ctx: The channel from which the user gave the command.
        '''
        if self.voiceChannel is not None and self.voiceChannel.is_connected() and self.voiceChannel.is_playing():
            self.voiceChannel.pause()
        else:
            await ctx.send("There is no song playing in order to pause it")

    async def resume_song(self, ctx):
        '''
        Resumes a song if there is one that has been paused or send a message if there is no such song
        :param ctx: The channel from which the user gave the command.
        '''
        if self.voiceChannel is not None and self.voiceChannel.is_connected() and self.voiceChannel.is_paused():
            self.voiceChannel.resume()
        else:
            await ctx.send("There is no song paused in order to resume it")

    async def stop(self, ctx):
        '''
        Stops the music if there is music or sends message if there is not. At the end clears the file of
        the unnecessary songs.
        :param ctx: The channel from which the user gave the command.
        '''
        if self.voiceChannel is not None and self.voiceChannel.is_connected() and self.voiceChannel.is_playing():
            self.voiceChannel.stop()
        else:
            await ctx.send("There is no song playing in order to stop it")
        self.clear_folder()

    async def next(self, ctx):
        '''
        Stops this song and start the next one. The user will be informed with message if there is no other song or if
        there is no song playing at the moment
        :param ctx: The channel from which the user gave the command.
        '''
        if self.voiceChannel is not None and self.voiceChannel.is_connected() and self.voiceChannel.is_playing() \
                and self.queue:
            await self.stop(ctx)
            self.load_next_song()
        elif not self.queue:
            await ctx.send("There is no other song in the queue")
        else:
            await ctx.send("There is no song playing, maybe use $play to start playing songs from the queue")

    async def play(self, ctx, channel):
        '''
        Starts playing the first song in the queue. If there are not songs in the queue or there is some music playing
        at this moment the user will ne informed with messages
        :param ctx: The channel from which the user gave the command.
        '''
        await self.connect(channel)
        if self.voiceChannel is not None and self.voiceChannel.is_connected() and not self.voiceChannel.is_playing()\
                and self.queue:
            self.load_next_song()
        elif not self.queue:
            await ctx.send("There is no song in the list")
        elif self.voiceChannel.is_playing():
            await ctx.send("THere is already some music playing. Increase the volume and join the party!")
