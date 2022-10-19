#ifndef NODEMANAGER_H
#define NODEMANAGER_H

#include <QMainWindow>

namespace Ui {
class NodeManager;
}

class NodeManager : public QMainWindow
{
    Q_OBJECT

public:
    explicit NodeManager(QWidget *parent = nullptr);
    ~NodeManager();

private:
    Ui::NodeManager *ui;
};

#endif // NODEMANAGER_H
