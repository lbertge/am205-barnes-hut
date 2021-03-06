/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

#include "glwidget.h"
#include <QPainter>
#include <QTimer>
#include "QFile"
#include "QDir"
#include <iostream>
#include <string>
#include <sstream>

#include <QPainter>
#include <QPaintEvent>
//! [0]
GLWidget::GLWidget(QWidget *parent)
    : QOpenGLWidget(parent)
{
    elapsed = 0;
    index = 0;
    setFixedSize(1000, 1000);
    setAutoFillBackground(false);
//    QFile file("/Users/alexkashi/Documents/Processing/barnesHut/result2.csv");
       QFile file("/Users/alexkashi/Harvard/AM205/am205-barnes-hut/output/result-2021-12-14-20-38.csv");
    if(!file.open(QIODevice::ReadOnly)) {
//            QDebug() << "Error reading file";
    }

    QTextStream in(&file);

    while(!in.atEnd()) {
        QString line = in.readLine();
        QStringList pieces = line.split(",");
        QVector<QPointF> timePoint;
        float tmp_x, tmp_y;

        for(int i = 0; i < pieces.size(); i+=2){
            std::istringstream StrToFloat(pieces.at(i).toStdString());
            StrToFloat >> tmp_x;
            std::istringstream StrToFloat2(pieces.at(i+1).toStdString());
            StrToFloat2 >> tmp_y;

            timePoint.append(QPointF(400 + tmp_x ,200 + tmp_y ));
        }
        data.append(timePoint);
    }
    file.close();
}

void GLWidget::animate()
{
    elapsed = (elapsed + qobject_cast<QTimer*>(sender())->interval()) % 1000;
    index +=5;
    update();
}

void GLWidget::paintEvent(QPaintEvent *event)
{

    QPainter painter;
    painter.begin(this);
    painter.setRenderHint(QPainter::Antialiasing);
    painter.setBrush(Qt::white);
    painter.fillRect(event->rect(), QBrush(QColor(0, 0, 0)));
    for(int i = std::max(0, index - 50); i < index; i++){
        for(QPointF point : data[i % data.length()]){
            painter.setBrush(QBrush(QColor(255,255,255)));
            painter.drawEllipse(point, 3,3);
        }
    }
    painter.end();
}

