/****************************************************************************
** Meta object code from reading C++ file 'scatterdatamodifier.h'
**
** Created by: The Qt Meta Object Compiler version 68 (Qt 6.2.2)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../3d/scatterdatamodifier.h"
#include <QtDataVisualization/q3dscene.h>
#include <QtDataVisualization/qscatter3dseries.h>
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'scatterdatamodifier.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 68
#error "This file was generated using the moc from 6.2.2. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_ScatterDataModifier_t {
    const uint offsetsAndSize[34];
    char stringdata0[250];
};
#define QT_MOC_LITERAL(ofs, len) \
    uint(offsetof(qt_meta_stringdata_ScatterDataModifier_t, stringdata0) + ofs), len 
static const qt_meta_stringdata_ScatterDataModifier_t qt_meta_stringdata_ScatterDataModifier = {
    {
QT_MOC_LITERAL(0, 19), // "ScatterDataModifier"
QT_MOC_LITERAL(20, 24), // "backgroundEnabledChanged"
QT_MOC_LITERAL(45, 0), // ""
QT_MOC_LITERAL(46, 7), // "enabled"
QT_MOC_LITERAL(54, 18), // "gridEnabledChanged"
QT_MOC_LITERAL(73, 20), // "shadowQualityChanged"
QT_MOC_LITERAL(94, 7), // "quality"
QT_MOC_LITERAL(102, 11), // "fontChanged"
QT_MOC_LITERAL(114, 4), // "font"
QT_MOC_LITERAL(119, 11), // "changeStyle"
QT_MOC_LITERAL(131, 5), // "style"
QT_MOC_LITERAL(137, 11), // "changeTheme"
QT_MOC_LITERAL(149, 5), // "theme"
QT_MOC_LITERAL(155, 19), // "changeShadowQuality"
QT_MOC_LITERAL(175, 28), // "shadowQualityUpdatedByVisual"
QT_MOC_LITERAL(204, 31), // "QAbstract3DGraph::ShadowQuality"
QT_MOC_LITERAL(236, 13) // "shadowQuality"

    },
    "ScatterDataModifier\0backgroundEnabledChanged\0"
    "\0enabled\0gridEnabledChanged\0"
    "shadowQualityChanged\0quality\0fontChanged\0"
    "font\0changeStyle\0style\0changeTheme\0"
    "theme\0changeShadowQuality\0"
    "shadowQualityUpdatedByVisual\0"
    "QAbstract3DGraph::ShadowQuality\0"
    "shadowQuality"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_ScatterDataModifier[] = {

 // content:
      10,       // revision
       0,       // classname
       0,    0, // classinfo
       8,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       4,       // signalCount

 // signals: name, argc, parameters, tag, flags, initial metatype offsets
       1,    1,   62,    2, 0x06,    1 /* Public */,
       4,    1,   65,    2, 0x06,    3 /* Public */,
       5,    1,   68,    2, 0x06,    5 /* Public */,
       7,    1,   71,    2, 0x06,    7 /* Public */,

 // slots: name, argc, parameters, tag, flags, initial metatype offsets
       9,    1,   74,    2, 0x0a,    9 /* Public */,
      11,    1,   77,    2, 0x0a,   11 /* Public */,
      13,    1,   80,    2, 0x0a,   13 /* Public */,
      14,    1,   83,    2, 0x0a,   15 /* Public */,

 // signals: parameters
    QMetaType::Void, QMetaType::Bool,    3,
    QMetaType::Void, QMetaType::Bool,    3,
    QMetaType::Void, QMetaType::Int,    6,
    QMetaType::Void, QMetaType::QFont,    8,

 // slots: parameters
    QMetaType::Void, QMetaType::Int,   10,
    QMetaType::Void, QMetaType::Int,   12,
    QMetaType::Void, QMetaType::Int,    6,
    QMetaType::Void, 0x80000000 | 15,   16,

       0        // eod
};

void ScatterDataModifier::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<ScatterDataModifier *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->backgroundEnabledChanged((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 1: _t->gridEnabledChanged((*reinterpret_cast< bool(*)>(_a[1]))); break;
        case 2: _t->shadowQualityChanged((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->fontChanged((*reinterpret_cast< const QFont(*)>(_a[1]))); break;
        case 4: _t->changeStyle((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 5: _t->changeTheme((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 6: _t->changeShadowQuality((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 7: _t->shadowQualityUpdatedByVisual((*reinterpret_cast< QAbstract3DGraph::ShadowQuality(*)>(_a[1]))); break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (ScatterDataModifier::*)(bool );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&ScatterDataModifier::backgroundEnabledChanged)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (ScatterDataModifier::*)(bool );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&ScatterDataModifier::gridEnabledChanged)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (ScatterDataModifier::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&ScatterDataModifier::shadowQualityChanged)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (ScatterDataModifier::*)(const QFont & );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&ScatterDataModifier::fontChanged)) {
                *result = 3;
                return;
            }
        }
    }
}

const QMetaObject ScatterDataModifier::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_ScatterDataModifier.offsetsAndSize,
    qt_meta_data_ScatterDataModifier,
    qt_static_metacall,
    nullptr,
qt_incomplete_metaTypeArray<qt_meta_stringdata_ScatterDataModifier_t
, QtPrivate::TypeAndForceComplete<ScatterDataModifier, std::true_type>, QtPrivate::TypeAndForceComplete<void, std::false_type>, QtPrivate::TypeAndForceComplete<bool, std::false_type>, QtPrivate::TypeAndForceComplete<void, std::false_type>, QtPrivate::TypeAndForceComplete<bool, std::false_type>, QtPrivate::TypeAndForceComplete<void, std::false_type>, QtPrivate::TypeAndForceComplete<int, std::false_type>, QtPrivate::TypeAndForceComplete<void, std::false_type>, QtPrivate::TypeAndForceComplete<const QFont &, std::false_type>
, QtPrivate::TypeAndForceComplete<void, std::false_type>, QtPrivate::TypeAndForceComplete<int, std::false_type>, QtPrivate::TypeAndForceComplete<void, std::false_type>, QtPrivate::TypeAndForceComplete<int, std::false_type>, QtPrivate::TypeAndForceComplete<void, std::false_type>, QtPrivate::TypeAndForceComplete<int, std::false_type>, QtPrivate::TypeAndForceComplete<void, std::false_type>, QtPrivate::TypeAndForceComplete<QAbstract3DGraph::ShadowQuality, std::false_type>


>,
    nullptr
} };


const QMetaObject *ScatterDataModifier::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *ScatterDataModifier::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_ScatterDataModifier.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int ScatterDataModifier::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 8)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 8;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 8)
            *reinterpret_cast<QMetaType *>(_a[0]) = QMetaType();
        _id -= 8;
    }
    return _id;
}

// SIGNAL 0
void ScatterDataModifier::backgroundEnabledChanged(bool _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void ScatterDataModifier::gridEnabledChanged(bool _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void ScatterDataModifier::shadowQualityChanged(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void ScatterDataModifier::fontChanged(const QFont & _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 3, _a);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE
