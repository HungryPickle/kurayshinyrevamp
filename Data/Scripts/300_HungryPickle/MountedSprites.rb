class MountedSprites
  @directory = "MountedSprites"
  @loaded_custom_folders = Array.new(Settings::NB_POKEMON)
  @loaded_autogen_folders = Array.new(Settings::NB_POKEMON)


  def self.set_folder
    if !safeIsDirectory?(@directory)
      @directory = Dir["MountedSprites"].first
      #echoln(@directory)
    end
  end

  def self.load_base_sprites
    return if !@directory
    #echoln("#{@directory}/base_sprites.pickle")
    System.mount("#{@directory}/base_sprites.pickle", Settings::CUSTOM_BASE_SPRITES_FOLDER)
  end

  def self.load_custom_sprites(head_id)
    #echoln("#{@directory}/custom_sprites/#{head_id}.pickle")
    System.mount(("#{@directory}/custom_sprites/#{head_id}.pickle").to_s, Settings::CUSTOM_BATTLERS_FOLDER_INDEXED)
    @loaded_custom_folders[head_id] = 1
  end

  def self.load_autogen_sprites(head_id)
    #echoln("#{@directory}/autogen_sprites/#{head_id}.pickle")
    System.mount(("#{@directory}/autogen_sprites/#{head_id}.pickle").to_s, Settings::BATTLERS_FOLDER)
    @loaded_autogen_folders[head_id] = 1
  end

  def self.resolve_path(path)
    return nil if !@directory
    return nil if path.include?("_i")
    return path if path.include?(Settings::CUSTOM_BASE_SPRITES_FOLDER)

    if path.include?(Settings::CUSTOM_BATTLERS_FOLDER_INDEXED)
      head_id = path[/(?<=\/)\d+(?=\/)/].to_i
      load_custom_sprites(head_id) if @loaded_custom_folders[head_id] != 1
      return path
    elsif path.include?(Settings::BATTLERS_FOLDER)
      head_id = path[/(?<=\/)\d+(?=\/)/].to_i
      load_autogen_sprites(head_id) if @loaded_autogen_folders[head_id] != 1
      return path
    end

    #echoln("Failed to resolve: #{path}")
    return nil
  end
end
