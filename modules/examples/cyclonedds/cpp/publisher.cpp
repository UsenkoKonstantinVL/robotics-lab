#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <thread>

#include <dds/dds.hpp>

#include "HelloMessage.hpp"

namespace {

constexpr auto kTopicName = "robotics_lab.examples.hello";

std::uint32_t message_count(int argc, char* argv[]) {
  if (argc < 2) {
    return 5;
  }
  return static_cast<std::uint32_t>(std::stoul(argv[1]));
}

}  // namespace

int main(int argc, char* argv[]) {
  try {
    const auto count = message_count(argc, argv);
    dds::domain::DomainParticipant participant(
        org::eclipse::cyclonedds::domain::default_id());
    dds::topic::Topic<robotics_lab_examples::HelloMessage> topic(
        participant, kTopicName);
    dds::pub::Publisher publisher(participant);
    dds::pub::DataWriter<robotics_lab_examples::HelloMessage> writer(publisher,
                                                                     topic);

    std::this_thread::sleep_for(std::chrono::seconds(1));
    for (std::uint32_t sequence = 1; sequence <= count; ++sequence) {
      robotics_lab_examples::HelloMessage message(
          "cpp-publisher", sequence, "Hello from Cyclone DDS C++");
      writer.write(message);
      std::cout << "published sequence=" << sequence << " sender="
                << message.sender() << '\n';
      std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }
  } catch (const std::exception& error) {
    std::cerr << "publisher failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }

  return EXIT_SUCCESS;
}
