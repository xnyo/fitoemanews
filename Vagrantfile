# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/artful64"
  config.vm.network "private_network", ip: "172.16.10.100"

  # Sync .gitconfig and ssh keys in /home/vagrant to make git work in the VM
  config.vm.provision "file", run: "always", source: "~/.gitconfig", destination: "~/.gitconfig"
  config.vm.provision "file", run: "always", source: "~/.ssh", destination: "~/.ssh"
  
  scripts = []
  Dir.glob("vagrant/provisioners/*_*.sh").each do |file_path|
    file_name = file_path.split("/")[-1]
    file_name_parts = file_name.split("_")
    scripts.push({ "index" => Integer(file_name_parts[0]), "file_name" => file_name, "privileged" => file_name_parts[1] == "sudo" })
  end

  scripts = scripts.sort_by { |hsh| hsh["index"] }
  scripts.each do |script|
    $script = <<-SCRIPT
        set -e
        echo "@ Running #{script['file_name']}"
        bash "/vagrant/vagrant/provisioners/#{script['file_name']}"
        echo "@ #{script['file_name']} executed successfully!"
    SCRIPT
    config.vm.provision :shell,
      inline: $script, privileged: script["privileged"]
  end
end
