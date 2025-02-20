from ossapi import (
    Cursor,
    Ossapi,
    Statistics,
    UserLookupKey,
    GameMode,
    RankingType,
    Scope,
    mod,
)
from datetime import date, datetime, timedelta, timezone
from discord import Embed


client_id = 38046
client_secret = "OqOJNzxWdsb67mN4EREGebQQSx9vewCmBNSFoKEx"
callback_url = "http://localhost:4378/"
scopes = [Scope.PUBLIC, Scope.FRIENDS_READ, Scope.IDENTIFY]
api = Ossapi(client_id, client_secret, callback_url, scopes=scopes)


def calculate_date(x):
    d = date.fromisoformat(x)
    t = date.today()
    s = date.__sub__(t, d)
    delta = timedelta.total_seconds(s)
    return delta


def get_id():
    name = input("Name: ")
    user = api.user(name, key=UserLookupKey.USERNAME)
    print(user.id)


def get_rank_n_player():
    top50 = api.ranking(GameMode.OSU, RankingType.PERFORMANCE)
    # can also use string version of enums
    top50 = api.ranking("osu", "performance")

    print(top50.ranking[1].user.username)  # mrekk as of 2022


def osfriends():
    print(api.friends())


def pagination():
    r = api.ranking("osu", RankingType.PERFORMANCE)
    cursor = r.cursor
    print(r.ranking[-1].global_rank)  # 50

    r = api.ranking("osu", RankingType.PERFORMANCE, cursor=cursor)
    print(r.ranking[-1].global_rank)  # 100

    cursor = Cursor(page=19)
    r = api.ranking("osu", RankingType.PERFORMANCE, cursor=cursor)
    print(r.ranking[-1].global_rank)  # 950


def check_lastpage():
    cursor = Cursor(page=199)
    r = api.ranking("osu", RankingType.PERFORMANCE, cursor=cursor)
    print(r.cursor)  # Cursor(page=200)

    cursor = Cursor(page=200)  # there are only 200 rankings pages
    r = api.ranking("osu", RankingType.PERFORMANCE, cursor=cursor)
    print(r.cursor)  # None


def ucomp():
    compact_user = api.search(query="tekaii").users.data[0]
    # `statistics` is only available on `User` not `UserCompact`,
    # so expansion is necessary
    full_user = compact_user.expand()
    print(full_user.statistics.ranked_score)


def bmap():
    beatmap = api.beatmap(221777)
    bmset = beatmap.beatmapset()
    print(bmset)


def get_me():
    user = api.get_me()
    x = get_user_info(user)
    e = user_embedder(x)
    return e


def get_user(uname):
    user = api.user(user=uname)
    x = get_user_info(user)
    e = user_embedder(x)
    return e


def get_user_info(user):
    username = user.username
    globrank = user.statistics.global_rank
    usrcountr = user.country.code
    userflag = f"https://osu.ppy.sh/images/flags/{usrcountr}.png"
    globrankhighest = user.rank_highest.rank
    x = user.rank_highest.updated_at
    globalhighestdate = (datetime.now(timezone.utc) - x).days
    ucontrank = user.statistics.country_rank
    ulevel = user.statistics.level.current
    ulevelprog = user.statistics.level.progress
    upp = user.statistics.pp
    uacc = user.statistics.hit_accuracy
    uacc = f"{uacc:.2f}"
    uisonline = user.is_online
    usravatarurl = user.avatar_url
    website = f"https://osu.ppy.sh/users/{user.id}/"
    badges = len(user.badges)
    ss = user.statistics.grade_counts.ss
    ssh = user.statistics.grade_counts.ssh
    s = user.statistics.grade_counts.s
    sh = user.statistics.grade_counts.sh
    a = user.statistics.grade_counts.a

    return (
        username,  # 0
        website,
        userflag,  # 2
        globrank,  # 3
        ucontrank,
        usrcountr,  # 5
        globrankhighest,
        globalhighestdate,  # 7
        ulevel,
        ulevelprog,  # 9
        upp,
        uacc,  # 11
        uisonline,
        usravatarurl,  # 13
        badges,  # 14
        ss,
        ssh,
        s,
        sh,
        a,
    )


def user_embedder(x):
    embed = Embed(
        description=f"**Bancho Rank**:#{x[3]} ({x[5]}#{x[4]})\n"
        f"level:{x[8]} progress:{x[9]}\n"
        f"PP:{x[10]} acc:{x[11]}\n"
        f"badges: {x[14]}\n"
        f"SS:{x[15]} SSH:{x[16]} S:{x[17]} SH:{x[18]} A:{x[19]}"
    )
    embed.set_author(name=f"{x[0]}", url=x[1], icon_url=x[2])
    return embed


def me_recent_scores():
    username = api.user(api.get_me().username, key=UserLookupKey.USERNAME)
    score = api.user_scores(user_id=username.id, type="recent", limit=1)
    print(score)


def user_recent_score():
    userinput = input("Input player name: ")
    username = api.user(userinput, key=UserLookupKey.USERNAME)
    scores = api.user_scores(
        user_id=username.id, include_fails=True, type="recent", limit=1
    )
    for score in scores:
        sgrade = score.rank
        acc = score.accuracy
        sctime = score.ended_at
        scmaxcom = score.max_combo
        bmapurl = score.beatmap.url
        scplayer = score._user.username
        scpp = score.pp
        mods = score.mods

        return (sgrade, acc, sctime, scmaxcom, bmapurl, scpp, scplayer, mods)
