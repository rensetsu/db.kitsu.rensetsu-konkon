from librensetsu.prettyprint import PrettyPrint, Platform, Status

pprint = PrettyPrint(Platform.SYSTEM)
PLATFORM = ""
RAW_DB = f"{PLATFORM}_raw.json"
DEST = f"{PLATFORM}.json"
DESTM = f"{PLATFORM}_min.json"

__all__ = ['pprint', 'Platform', 'Status', 'RAW_DB', 'DEST', 'DESTM']
