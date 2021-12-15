/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the Qt Data Visualization module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:GPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3 or (at your option) any later version
** approved by the KDE Free Qt Foundation. The licenses are as published by
** the Free Software Foundation and appearing in the file LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

#include "scatterdatamodifier.h"
#include <QtDataVisualization/qscatterdataproxy.h>
#include <QtDataVisualization/qvalue3daxis.h>
#include <QtDataVisualization/q3dscene.h>
#include <QtDataVisualization/q3dcamera.h>
#include <QtDataVisualization/qscatter3dseries.h>
#include <QtDataVisualization/q3dtheme.h>
#include <QtCore/qmath.h>
#include <QtCore/qrandom.h>
#include <QtWidgets/QComboBox>
#include <QPainter>
#include <QTimer>
#include "QFile"
#include "QDir"
#include <iostream>
#include <string>
#include <sstream>

#include <QPainter>
#include <QPaintEvent>
//#define RANDOM_SCATTER // Uncomment this to switch to random scatter

const int numberOfItems = 3600;
const float curveDivider = 3.0f;
const int lowerNumberOfItems = 900;
const float lowerCurveDivider = 0.75f;

ScatterDataModifier::ScatterDataModifier(Q3DScatter *scatter)
    : m_graph(scatter),
      m_fontSize(40.0f),
      m_style(QAbstract3DSeries::MeshSphere),
      m_smooth(true),
      m_itemCount(lowerNumberOfItems),
      m_curveDivider(lowerCurveDivider)
{
    //! [0]
    m_graph->activeTheme()->setType(Q3DTheme::ThemeEbony);
    QFont font = m_graph->activeTheme()->font();
    font.setPointSize(m_fontSize);
    m_graph->activeTheme()->setFont(font);
    m_graph->setShadowQuality(QAbstract3DGraph::ShadowQualitySoftLow);
    m_graph->scene()->activeCamera()->setCameraPreset(Q3DCamera::CameraPresetFront);

    index = 0;

    colors.push_back(Qt::yellow);

    colors.push_back(Qt::red);

    colors.push_back(Qt::darkYellow);

    colors.push_back(Qt::blue);
    colors.push_back(Qt::white);

    colors.push_back(Qt::darkRed);

//    QFile file("/Users/alexkashi/Documents/Processing/barnesHut/result2.csv");
//    QFile file("/Users/alexkashi/Harvard/AM205/am205-barnes-hut/output/result-2021-12-14-22-31.csv");
        QFile file("C://Users//AlexKashi//Harvard//AM205//am205-barnes-hut//output//result-2021-12-15-03-49.csv");
    if(!file.open(QIODevice::ReadOnly)) {
//            QDebug() << "Error reading file";
    }

    QTextStream in(&file);
    int count = 0;

    float minX=0, maxX=0, minY = 0, maxY = 0, minZ = 0, maxZ = 0;
    while(!in.atEnd()) {
        QString line = in.readLine();
        QStringList pieces = line.split(",");
        QVector<QVector3D> timePoint;
        float tmp_x, tmp_y, tmp_z;
        bodyCount = 0;
        for(int i = 0; i < pieces.size(); i+=3){
            std::istringstream StrToFloat(pieces.at(i).toStdString());
            StrToFloat >> tmp_x;
            std::istringstream StrToFloat2(pieces.at(i+1).toStdString());
            StrToFloat2 >> tmp_y;

            std::istringstream StrToFloat3(pieces.at(i+2).toStdString());
            StrToFloat3 >> tmp_z;

            minX = std::min(tmp_x, minX);
            maxX = std::max(tmp_x, maxX);
            minY = std::min(tmp_y, minY);
            maxY = std::max(tmp_y, maxY);
            minZ = std::min(tmp_z, minZ);
            maxZ = std::max(tmp_z, maxZ);

            bodyCount++;
            timePoint.append(QVector3D(tmp_x,tmp_y,tmp_z));
        }
//        if(itterCount > 1000){
//            break;
//        }
        itterCount++;
        data.append(timePoint);
    }
    file.close();

    dataArray2 = new QScatterDataArray;
    QScatterDataProxy *proxy = new QScatterDataProxy;
    QScatter3DSeries *series = new QScatter3DSeries(proxy);
    series->setItemLabelFormat(QStringLiteral("@xTitle: @xLabel @yTitle: @yLabel @zTitle: @zLabel"));
    series->setMeshSmooth(m_smooth);
    series->setItemSize(0.1f);
    m_graph->addSeries(series);
    m_graph->axisX()->setMin(minX);
    m_graph->axisX()->setMax(maxX);
    m_graph->axisY()->setMin(minY);
    m_graph->axisY()->setMax(maxY);
    m_graph->axisZ()->setMin(minZ);
    m_graph->axisZ()->setMax(maxZ);
    m_graph->axisX()->setLabelFormat(" ");
    m_graph->axisY()->setLabelFormat(" ");
    m_graph->axisZ()->setLabelFormat(" ");

    m_graph->addSeries(new QScatter3DSeries);
    m_graph->addSeries(new QScatter3DSeries);
    m_graph->addSeries(new QScatter3DSeries);
    m_graph->addSeries(new QScatter3DSeries);
    m_graph->addSeries(new QScatter3DSeries);


//    dataArray = new QScatterDataArray;
//    addData();
    //! [3]
}

ScatterDataModifier::~ScatterDataModifier()
{
    delete m_graph;
}

//! [8]
void ScatterDataModifier::changeStyle(int style)
{
    QComboBox *comboBox = qobject_cast<QComboBox *>(sender());
    if (comboBox) {
        m_style = QAbstract3DSeries::Mesh(comboBox->itemData(style).toInt());
        if (m_graph->seriesList().size())
            m_graph->seriesList().at(0)->setMesh(m_style);
    }
}

void ScatterDataModifier::setSmoothDots(int smooth)
{
    m_smooth = bool(smooth);
    QScatter3DSeries *series = m_graph->seriesList().at(0);
    series->setMeshSmooth(m_smooth);
}

void ScatterDataModifier::changeTheme(int theme)
{
    Q3DTheme *currentTheme = m_graph->activeTheme();
    currentTheme->setType(Q3DTheme::Theme(theme));
    emit backgroundEnabledChanged(currentTheme->isBackgroundEnabled());
    emit gridEnabledChanged(currentTheme->isGridEnabled());
    emit fontChanged(currentTheme->font());
}
void ScatterDataModifier::animate()
{



    for (int i = 0; i < bodyCount; i++) {
        QScatterDataArray *dataArray = new QScatterDataArray;

        *dataArray << data[index % data.length()][i];
        dataArray->resize(1);
         m_graph->seriesList().at(i)->dataProxy()->resetArray(dataArray);
            m_graph->seriesList().at(i)->setMeshSmooth(true);
        m_graph->seriesList().at(i)->setItemSize(0.1f);
        m_graph->seriesList().at(i)->setBaseColor(colors[i% colors.length()]);

//        QScatterDataItem *ptrToDataArray = &dataArray->first();
//           scatter.seriesList().at(1)->setBaseColor(Qt::green);

//        ptrToDataArray->setPosition(data[index % data.length()][i]);
//        ptrToDataArray++;
    }
//    m_graph->seriesList().at(0)->dataProxy()->resetArray(dataArray);
    index +=500;

//    QLinearGradient linearGrad(QPointF(100, 100), QPointF(200, 200));
//    linearGrad.setColorAt(0, Qt::blue);
//    linearGrad.setColorAt(1, Qt::red);

//    m_graph->seriesList().at(0)->setBaseGradient(linearGrad);
//    m_graph->seriesList().at(0)->setColorStyle(Q3DTheme::ColorStyle::ColorStyleObjectGradient);

}
void ScatterDataModifier::changePresetCamera()
{
    static int preset = Q3DCamera::CameraPresetFrontLow;

    m_graph->scene()->activeCamera()->setCameraPreset((Q3DCamera::CameraPreset)preset);

    if (++preset > Q3DCamera::CameraPresetDirectlyBelow)
        preset = Q3DCamera::CameraPresetFrontLow;
}

void ScatterDataModifier::changeLabelStyle()
{
    m_graph->activeTheme()->setLabelBackgroundEnabled(!m_graph->activeTheme()->isLabelBackgroundEnabled());
}

void ScatterDataModifier::changeFont(const QFont &font)
{
    QFont newFont = font;

    newFont.setPointSizeF(0.001);
    m_graph->activeTheme()->setFont(newFont);
}

void ScatterDataModifier::shadowQualityUpdatedByVisual(QAbstract3DGraph::ShadowQuality sq)
{
    int quality = int(sq);
    emit shadowQualityChanged(quality); // connected to a checkbox in main.cpp
}

void ScatterDataModifier::changeShadowQuality(int quality)
{
    QAbstract3DGraph::ShadowQuality sq = QAbstract3DGraph::ShadowQuality(quality);
    m_graph->setShadowQuality(sq);
}

void ScatterDataModifier::setBackgroundEnabled(int enabled)
{
    m_graph->activeTheme()->setBackgroundEnabled((bool)enabled);
}

void ScatterDataModifier::setGridEnabled(int enabled)
{
    m_graph->activeTheme()->setGridEnabled((bool)enabled);
}
//! [8]


