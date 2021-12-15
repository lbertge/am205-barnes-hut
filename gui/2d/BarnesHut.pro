QT += widgets opengl openglwidgets

HEADERS     = glwidget.h \
              window.h
SOURCES     = glwidget.cpp \
              main.cpp \
              window.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/opengl/2dpainting
INSTALLS += target
