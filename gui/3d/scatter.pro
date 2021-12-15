android|ios|winrt {
    error( "This example is not supported for android, ios, or winrt." )
}

!include( ../examples.pri ) {
    error( "Couldn't find the examples.pri file!" )
}

SOURCES += main.cpp scatterdatamodifier.cpp \
    window.cpp
HEADERS += scatterdatamodifier.h \
    window.h

QT += widgets
requires(qtConfig(combobox))
requires(qtConfig(fontcombobox))

OTHER_FILES += doc/src/* \
               doc/images/*
