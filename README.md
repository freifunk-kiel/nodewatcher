Nodewatcher
===========

This software is supposed to watch a network of Freifunk nodes and notify their
owners if their nodes go down.

It is modularized so that it can take the node status from various sources
(currently only A.L.F.R.E.D., as used in [gluon]) and notify via various
methods (see below).

[gluon]: https://github.com/freifunk-gluon/gluon/

Contact methods
---------------

Depending on the source, the owners provide means of contact. These may be any of the following methods:

Method     | URI scheme
-----------|-------------------------------------------------
E-Mail     | mailto:mail@example.org or just mail@example.org
XMPP       | xmpp:jabber@example.org
IRC        | irc://irc.example.org/channel or irc://irc.example.org/nick,isnick
Twitter DM | @TwitterUsername

Multiple contact methods can be specified separated by ", " (without quotes).

Requirements
------------

The required Python3 packages are

* SQLAlchemy
* sleekxmpp ≥1.0 (for the XMPP notification plugin)
* TwitterAPI twython (for the Twitter notification plugin)
* [IRClib](https://bitbucket.org/jaraco/irc) (for the IRC notification plugin)

On Debian systems install via apt with:

    apt-get install python3-sqlalchemy python3-sleekxmpp python3-twython


Setup
-----

    git clone http://github.com/<this repositroy>/nodewatcher
    cd nodewatcher
    cp config.sample.py config.py

and adept `config.py` to your needs.

Then execute:

    python3

```python
from db import Base, engine
Base.metadata.create_all(engine)
```
to create the database structure. 

After that, all you need to do is call the `main.py`, for example via a cronjob in `/etc/cron.d/nodewatcher`:
```cron
*/5 * * * * root python3 /usr/local/src/nodewatcher/main.py
```

Database Structure
------------------

- id = internal ID for each node
- name = hostname of the node
- lastseen = Timestamp from nodes.json
- contact = owner String given in the config mode of the node
- lastcontact = Timestamp, when the owner was contacted about his offline node
- ignore = default NULL, node owners will be sent notifications for their offline nodes:
 - if opt_in==True and ignore=="0"
 - if opt_in==False and (ignore=="0" or ignore==NULL)

Database Maintenance
--------------------

Install

    apt-get install sqlite3 sqlite3-pcre

so you can manipulate the database. Example:

```bash
sqlite3 nodes.db -header "select id, name, contact, lastcontact, ignore, datetime(lastseen, 'unixepoch', 'localtime') from nodes order by lastseen limit 5"

```
