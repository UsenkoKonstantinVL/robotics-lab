#include <algorithm>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <memory>
#include <sstream>
#include <string>

#include <dds/dds.hpp>

#include "ControlCommand.hpp"
#include "cpptui.hpp"

namespace {

constexpr auto kTopicName = "robotics_lab.control.command";
constexpr int kArrowUp = 1065;
constexpr int kArrowDown = 1066;
constexpr int kArrowRight = 1067;
constexpr int kArrowLeft = 1068;
constexpr float kSpeedStep = 0.1F;
constexpr int kPublishPeriodMs = 100;

std::string format_value(const std::string& name, float value) {
  std::ostringstream text;
  text << name << std::fixed << std::setprecision(1) << value;
  return text.str();
}

}  // namespace

int main() {
  try {
    dds::domain::DomainParticipant participant(
        org::eclipse::cyclonedds::domain::default_id());
    dds::topic::Topic<robotics_lab_types::ControlCommand> topic(participant,
                                                                kTopicName);
    dds::pub::Publisher publisher(participant);
    dds::pub::DataWriter<robotics_lab_types::ControlCommand> writer(publisher,
                                                                    topic);

    cpptui::Theme::set_theme(cpptui::Theme::Dark());
    cpptui::App app;
    auto root = std::make_shared<cpptui::Vertical>();
    auto title = std::make_shared<cpptui::Label>("Robotics Lab manual control");
    auto speed_label = std::make_shared<cpptui::Label>("Maximum speed: 1.0");
    auto command_label = std::make_shared<cpptui::Label>("Command: 0.0");

    root->add(title);
    root->add(std::make_shared<cpptui::VerticalSpacer>(1));
    root->add(std::make_shared<cpptui::Label>(
        "Up/Down: forward/reverse | Left/Right: adjust maximum speed"));
    root->add(std::make_shared<cpptui::Label>(
        "Release arrows to send zero | q: quit"));
    root->add(std::make_shared<cpptui::VerticalSpacer>(1));
    root->add(speed_label);
    root->add(command_label);

    float maximum_speed = 1.0F;
    float pending_command = 0.0F;

    app.register_key(kArrowUp, [&] { pending_command = maximum_speed; });
    app.register_key(kArrowDown, [&] { pending_command = -maximum_speed; });
    app.register_key(kArrowLeft, [&] {
      maximum_speed = std::max(0.0F, maximum_speed - kSpeedStep);
      speed_label->set_text(format_value("Maximum speed: ", maximum_speed));
    });
    app.register_key(kArrowRight, [&] {
      maximum_speed = std::min(1.0F, maximum_speed + kSpeedStep);
      speed_label->set_text(format_value("Maximum speed: ", maximum_speed));
    });
    app.register_exit_key('q');

    app.add_timer(kPublishPeriodMs, [&] {
      writer.write(robotics_lab_types::ControlCommand(pending_command));
      command_label->set_text(format_value("Command: ", pending_command));
      pending_command = 0.0F;
    });

    app.run(root);
    writer.write(robotics_lab_types::ControlCommand(0.0F));
  } catch (const std::exception& error) {
    std::cerr << "control TUI failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }

  return EXIT_SUCCESS;
}
