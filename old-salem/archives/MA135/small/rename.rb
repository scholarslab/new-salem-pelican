#! /usr/bin/env ruby

require 'FileUtils'
require 'awesome_print'

module Salem
  class Rename

    def initialize(path)
      @path = path
    end

    def path
      @path
    end

    def candidate?(file)
      /[\d]+\.[gif|jpg]+/.match(file).to_s.length > 0 ? true : false
    end

    def process
      Dir["#{path}*\.{jpg,gif}"].each do |file|
        if (candidate?(file))
          rename!(file)
        end
      end
    end

    private

    def rename!(file)
      basename = File.basename(file, ".*")
      extension = File.extname(file)

      dest_file = "MA#{basename}r#{extension}"

      FileUtils.cp file, "MA#{basename}r#{extension}", :verbose => true unless FileTest.exist?(dest_file)

      #FileUtils.mv file, "copy__#{basename}#{extension}"
    end

  end
end

rename = Salem::Rename.new('./')
ap rename.path
ap rename.process

