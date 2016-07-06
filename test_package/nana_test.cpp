#include <nana/gui.hpp>
#include <nana/gui/widgets/label.hpp>
#include <nana/gui/widgets/picture.hpp>
#include <nana/filesystem/filesystem.hpp> 
#include <nana/gui/timer.hpp>
#ifdef  NANA_ENABLE_AUDIO
	#include <nana/audio/player.hpp>
	#include <nana/threads/pool.hpp>
#endif //  NANA_AUDIO

#include <random>
#include <vector>

namespace fs = nana::experimental::filesystem;
std::vector<fs::path> get_files(const fs::path& base_path)
{
	std::vector<fs::path> files;
	fs::directory_iterator it_end{};
#ifdef NANA_ENABLE_PNG
	auto p = base_path.u8string() +  "/icons/png";
	fs::directory_iterator it_png{p};
	for (; it_png != it_end; ++it_png)
	{
		if (!fs::is_directory(it_png->path()))
		{
			files.emplace_back(it_png->path());
		}
	}
#endif
#ifdef NANA_ENABLE_JPEG
	auto p1 = base_path.u8string() + "/icons/jpeg";
	fs::directory_iterator it_jpeg{ p1 };
	for (; it_jpeg != it_end; ++it_jpeg)
	{
		if (!fs::is_directory(it_jpeg->path()))
		{
			files.emplace_back(it_jpeg->path());
		}
	}
#endif

	return files;
}



int main()
{
    using namespace nana;
	form fm{ API::make_center(480,48) };
	timer tm;
    //It's unnecessary to specify a rectangle if useing
    //layout management.
    label lb{ fm};

#ifdef NANA_ENABLE_AUDIO
	nana::audio::player player("../../sounds/113218__satrebor__click.wav");
	nana::threads::pool pool(1); //Only 1 thread.
#endif	


    lb.caption("Hello, world!");
    //Set a background color, just for observation.
    lb.bgcolor(colors::azure);
    //Define a layout object for the form.
//    place layout(fm);
    //The div-text
//    layout.div("<here>");
#if defined(NANA_ENABLE_PNG) || defined(NANA_ENABLE_JPEG)
	picture pic{ fm, rectangle{230, 0, 48, 48}};
	pic.tooltip("Click to change picture");
	auto vec_icons = get_files("../..");
	std::random_device rd;
	std::mt19937 g(rd());
	std::shuffle(vec_icons.begin(), vec_icons.end(), g);
	size_t ind = 1;
	pic.load(paint::image{vec_icons[0].wstring()});
	fm.caption(vec_icons[0].wstring());
	//layout["here"] << pic;

	tm.interval(5000);
	tm.start();

	auto next_image = [&]()
	{
		pic.load(paint::image{ vec_icons[ind].wstring() });
		fm.caption(vec_icons[ind].wstring());
		ind = ++ind % vec_icons.size();
	};

	tm.elapse([&](const nana::arg_elapse& e)
	{
		next_image();
	});

#ifdef NANA_ENABLE_AUDIO
	pic.events().click(threads::pool_push(pool, [&]()
	{
		player.play();
		next_image();
	}));
#else	
	pic.events().click([&]()
	{
		next_image();
	});
#endif
//    layout.collocate();
#endif

    fm.show();
    exec();
}