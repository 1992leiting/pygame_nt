#ifndef WINDOW_EDITOR_H
#define WINDOW_EDITOR_H

#include <QMainWindow>

namespace Ui {
class window_editor;
}

class window_editor : public QMainWindow
{
    Q_OBJECT

public:
    explicit window_editor(QWidget *parent = nullptr);
    ~window_editor();

private:
    Ui::window_editor *ui;
};

#endif // WINDOW_EDITOR_H
