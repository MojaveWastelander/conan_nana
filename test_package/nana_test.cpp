#include <nana/gui.hpp>
#include <nana/gui/widgets/label.hpp>
int main()
{
    using namespace nana;
    form fm;
    //It's unnecessary to specify a rectangle if useing
    //layout management.
    label lb{ fm};
    lb.caption("Hello, world!");
    //Set a background color, just for observation.
    lb.bgcolor(colors::azure);
    //Define a layout object for the form.
    place layout(fm);
    //The div-text
    layout.div("vert<><<><here weight=80><>><>");
    layout["here"] << lb;
    layout.collocate();
    fm.show();
    exec();
}