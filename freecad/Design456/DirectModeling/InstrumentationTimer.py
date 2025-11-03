from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2025                                                    *
# *                                                                        *
# *                                                                        *
# * This library is free software; you can redistribute it and/or          *
# * modify it under the terms of the GNU Lesser General Public             *
# * License as published by the Free Software Foundation; either           *
# * version 2 of the License, or (at your option) any later version.       *
# *                                                                        *
# * This library is distributed in the hope that it will be useful,        *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# * Lesser General Public License for more details.                        *
# *                                                                        *
# * You should have received a copy of the GNU Lesser General Public       *
# * License along with this library; if not, If not, see                   *
# * <http://www.gnu.org/licenses/>.                                        *
# *                                                                        *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

#
# Basic instrumentation profiler by Cherno Modified for python by Mariwan Jalal
# found here https://gist.github.com/TheCherno





import datetime
import time
import threading
import sys
from dataclasses import dataclass

#Struct in cpp
__updated__ = '2021-12-31 08:57:57'


class ProfileResult(object):
    def __init__(self):
        self.Name = ""
        self.Start = 0
        self.End = 0
        self.ThreadID = 0

#Struct in cpp
class InstrumentationSession(object):

    def __init__(self):
        self.Name = ""


class Instrumentor(object):
    def __init__(self):
        self.__m_CurrentSession = None
        self.__m_OutputStream = None
        self.__m_ProfileCount = 0
        self.current = self

    def BeginSession(self, name, filepath="D:/Users/Mavi/AppData/Roaming/FreeCAD/Mod/Design456/results.json"):
        print("BeginSession")
        self.__m_OutputStream = open(filepath, "w")
        self.WriteHeader()
        self.__m_CurrentSession = InstrumentationSession()
        self.__m_CurrentSession.name = name

    def EndSession(self):
        print("EndSession")
        self.WriteFooter()
        del self.__m_CurrentSession
        self.__m_CurrentSession = None
        self.__m_ProfileCount = 0
        self.current = None

    def WriteProfile(self, result):
        print("WriteProfile")
        if self.__m_ProfileCount > 0:
            self.__m_OutputStream.write(",")

        self.__m_ProfileCount += 1
        name = result.Name
        name.replace('"', '\'')
        self.__m_OutputStream.write("{")
        self.__m_OutputStream.write("\"cat\":\"function\",")
        self.__m_OutputStream.write(
            "\"dur\":" + str(result.End - result.Start) + ',')
        self.__m_OutputStream.write("\"name\":\"" + name + "\",")
        self.__m_OutputStream.write("\"ph\":\"X\",")
        self.__m_OutputStream.write("\"pid\":0,")
        self.__m_OutputStream.write("\"tid\":" + str(result.ThreadID) + ",")
        self.__m_OutputStream.write("\"ts\":" + str(result.Start))
        self.__m_OutputStream.write("}")
        self.__m_OutputStream.flush()

    def WriteHeader(self):
        print("writeHeader")
        self.__m_OutputStream.write("{\"otherData\": {},\"traceEvents\":[")
        self.__m_OutputStream.flush()

    def WriteFooter(self):
        print("writeFooter")
        self.__m_OutputStream.write("]}")
        self.__m_OutputStream.flush()

class InstrumentationTimer():
    def __init__(self, name):
        # instance fields found by C++ to Python Converter:
        self.__m_Stopped = False
        self.__m_Name = name
        self.__m_StartTimepoint =  datetime.datetime.now().microsecond #time.time_ns()
        self.current = None

    def __del__(self):
        print("Destructor")
        if not self.__m_Stopped:
            self.StopIt()

    def StopIt(self):
        print("stopit")
        endTimepoint = datetime.datetime.now().microsecond #time.time_ns()

        start = self.__m_StartTimepoint
        end = endTimepoint
        threadID = threading.current_thread().ident
        pro = ProfileResult()
        pro.Name = self.__m_Name
        pro.Start = start
        pro.End = end
        pro.ThreadID = threadID
        self.current.WriteProfile(pro)
        self.__m_Stopped = True
