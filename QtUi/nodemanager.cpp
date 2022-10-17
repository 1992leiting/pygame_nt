#include "nodemanager.h"
#include "ui_nodemanager.h"

NodeManager::NodeManager(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::NodeManager)
{
    ui->setupUi(this);
}

NodeManager::~NodeManager()
{
    delete ui;
}
