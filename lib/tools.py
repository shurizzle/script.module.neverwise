#!/usr/bin/python
# -*- coding: utf-8 -*-
# Version 1.0.0 (27/12/2013)
# NeverWise XBMC tools
# Strumenti per i plugins di xbmc.
# By NeverWise
# <email>
# <web>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################
import re, sys, urllib, urllib2, urlparse, xbmcplugin, xbmcgui, xbmcaddon, CommonFunctions


def getTranslation(addonId, translationId):
  return xbmcaddon.Addon(addonId).getLocalizedString(translationId).encode('utf-8')


def getResponseUrl(url):
  req = urllib2.Request(url)
  req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0')
  response = urllib2.urlopen(req)
  html = response.read()
  response.close()
  html = html.replace('\t', '').replace('\r\n', '').replace('\n', '').replace('\r', '').replace('" />', '"/>')
  while html.find('  ') > -1: html = html.replace('  ', ' ')
  return html


def normalizeText(text):
  text = text.strip().decode('utf8', 'xmlcharrefreplace')
  return CommonFunctions.replaceHTMLCodes(text)

def stripTags(html): return re.sub('<.+?>', '', html)

# Convert parameters encoded in a URL to a dict.
def urlParametersToDict(parameters):
  if len(parameters) > 0 and parameters[0] == '?':
    parameters = parameters[1:]
  return dict(urlparse.parse_qsl(parameters))


def createListItem(name, thumbimage, fanart, streamtype, infolabels):
  li = xbmcgui.ListItem(name, iconImage = 'DefaultFolder.png', thumbnailImage = thumbimage)
  li.setProperty('fanart_image', fanart)
  li.setInfo(streamtype, infolabels)
  return li


def addItem(handle, name, thumbimage, fanart, streamtype, infolabels, url, isFolder):
  li = createListItem(name, thumbimage, fanart, streamtype, infolabels)
  return xbmcplugin.addDirectoryItem(handle = handle, url = url, listitem = li, isFolder = isFolder)


def addLink(handle, name, thumbimage, fanart, streamtype, infolabels, url):
  return addItem(handle, name, thumbimage, fanart, streamtype, infolabels, url, False)


def addDir(handle, name, thumbimage, fanart, streamtype, infolabels, params):
  u = sys.argv[0] + '?' + urllib.urlencode(params)
  return addItem(handle, name, thumbimage, fanart, streamtype, infolabels, u, True)