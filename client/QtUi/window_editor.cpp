#include "window_editor.h"
#include "ui_window_editor.h"

window_editor::window_editor(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::window_editor)
{
    ui->setupUi(this);
}

window_editor::~window_editor()
{
    delete ui;
}
