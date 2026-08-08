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
    const auto expected_count = message_count(argc, argv);
    dds::domain::DomainParticipant participant(
        org::eclipse::cyclonedds::domain::default_id());
    dds::topic::Topic<robotics_lab_examples::HelloMessage> topic(
        participant, kTopicName);
    dds::sub::Subscriber subscriber(participant);
    dds::sub::DataReader<robotics_lab_examples::HelloMessage> reader(subscriber,
                                                                     topic);

    std::uint32_t received_count = 0;
    const auto deadline =
        std::chrono::steady_clock::now() + std::chrono::seconds(10);
    while (received_count < expected_count &&
           std::chrono::steady_clock::now() < deadline) {
      for (const auto& sample : reader.take()) {
        if (!sample.info().valid()) {
          continue;
        }
        const auto& message = sample.data();
        std::cout << "received sequence=" << message.sequence_number()
                  << " sender=" << message.sender() << " text=\""
                  << message.text() << "\"\n";
        ++received_count;
      }
      std::this_thread::sleep_for(std::chrono::milliseconds(20));
    }

    if (received_count != expected_count) {
      std::cerr << "subscriber timed out after receiving " << received_count
                << " of " << expected_count << " messages\n";
      return EXIT_FAILURE;
    }
  } catch (const std::exception& error) {
    std::cerr << "subscriber failed: " << error.what() << '\n';
    return EXIT_FAILURE;
  }

  return EXIT_SUCCESS;
}
