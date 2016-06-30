#include <nana/gui.hpp>
#include <nana/gui/widgets/label.hpp>
#include <nana/gui/widgets/picture.hpp>
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
#ifdef NANA_ENABLE_PNG
	picture pic{ fm };
	pic.load(paint::image("../../folder.png"));
	layout["here"] << pic;
#else
    layout["here"] << lb;
#endif
    layout.collocate();
    fm.show();
    exec();
}