import sqlite3,  zlib

class Serializer:

    # Constructor
    def __init__(self, target):
        self.name = "Worlds/" + target + '.db'
        self.conn = sqlite3.connect(self.name)
        c = self.conn.cursor()
        try:
            # Create Table
            c.execute('''CREATE TABLE terrain(keys INTEGER NOT NULL PRIMARY KEY, binry TEXT)''')
            self.conn.commit()
            c.execute('''CREATE TABLE player(playername TEXT NOT NULL PRIMARY KEY, pickledplayer TEXT)''')
            self.conn.commit()
        except:
            pass

    # Save magic method
    def __setitem__(self, key, chunkObj):
        """
            Saves/Updates the string at a particular key location.
            Requires the key as an int and chunkObj as UTF-8 string.
        """
        c = self.conn.cursor()
        try:
            # Save string at new key location
            c.execute('''INSERT INTO terrain VALUES (?,?)''', (key, zlib.compress(chunkObj, level = 9)))
            self.conn.commit()

        except:
            # Update string at existing key
            c.execute('UPDATE terrain SET binry =?  WHERE keys=?', (zlib.compress(chunkObj, level = 9), key))
            self.conn.commit()

    # Load magic method
    def __getitem__(self, key):
        """
            Retrieves the string stored at a particular key location.
            Requires the key as an int.
            Returns the string at the key's location (if key is present) or None
        """
        c = self.conn.cursor()
        c.execute('''SELECT binry FROM terrain WHERE keys=?''', (key,))
        res = c.fetchone()
        self.conn.commit()

        try: return zlib.decompress(res[0])
        except: return res

    def savePlayer(self, name, pickled):

        """
            Saves/Updates the pickledplayer at a particular playername.
            Requires the name as a string and pickled as UTF-8 string.
        """
        c = self.conn.cursor()
        try:
            # Save pickledplayer at new playername
            c.execute('''INSERT INTO player VALUES (?,?)''', (name, zlib.compress(pickled)))
            self.conn.commit()

        except:
            # Update pickledplayer at existing playername
            c.execute('UPDATE player SET pickledplayer =?  WHERE playername=?', (zlib.compress(pickled), name))
            self.conn.commit()

    def loadPlayer(self, name):

        """
            Retrieves the pickledplayer stored at a particular playername.
            Requires the name as a string.
            Returns the pickledplayer at the playername's location (if present) or None
        """
        c = self.conn.cursor()
        c.execute('''SELECT pickledplayer FROM player WHERE playername=?''', (name,))
        res = c.fetchone()
        self.conn.commit()

        try: return zlib.decompress(res[0])
        except: return res

    # Close the connection
    def stop(self):
        self.conn.close()

