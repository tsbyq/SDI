require 'openstudio'
require 'openstudio-standards'
require './measure.rb'


# Create a set of models, return a list of failures
def create_models(bldg_types, vintages, climate_zones, epw_files = [])
  #### Create the prototype building
  failures = []

  # Loop through all of the given combinations
  bldg_types.sort.each do |building_type|
    vintages.sort.each do |template|
      climate_zones.sort.each do |climate_zone|
        model_name = "#{building_type}-#{template}-#{climate_zone}"

        # Create an instance of the measure
        measure = CreateDOEPrototypeBuilding.new

        # Create an instance of a runner
        runner = OpenStudio::Measure::OSRunner.new(OpenStudio::WorkflowJSON.new)

        # Make an empty model
        model = OpenStudio::Model::Model.new

        # Set argument values
        arguments = measure.arguments(model)
        argument_map = OpenStudio::Measure::OSArgumentMap.new
        building_type_arg = arguments[0].clone
        argument_map['building_type'] = building_type_arg

        template_arg = arguments[1].clone
        argument_map['template'] = template_arg

        climate_zone_arg = arguments[2].clone
        argument_map['climate_zone'] = climate_zone_arg

        epw_arg = arguments[3].clone
        argument_map['epw_file'] = epw_arg

        measure.run(model, runner, argument_map)
        result = runner.result
        show_output(result)
        if result.value.valueName != 'Success'
          failures << "Error - #{model_name} - Model was not created successfully."
        end

        model_directory = "#{@test_dir}/#{building_type}-#{template}-#{climate_zone}"

        # Convert the model to energyplus idf
        forward_translator = OpenStudio::EnergyPlus::ForwardTranslator.new
        idf = forward_translator.translateModel(model)
        idf_path_string = "#{model_directory}/#{model_name}.idf"
        idf_path = OpenStudio::Path.new(idf_path_string)
        idf.save(idf_path, true)

        print(idf_path)
      end
    end
  end

  #### Return the list of failures
  return failures
end


def main
  bldg_types = ['PrimarySchool']
  vintages = ['DOE Ref Pre-1980'] # , 'DOE Ref 1980-2004', '90.1-2004', '90.1-2007', '90.1-2010']
  climate_zones = ['ASHRAE 169-2006-3A']
  create_models(bldg_types, vintages, climate_zones)
end


main()

def test
  
  building_type = 'SecondarySchool'
  template = '90.1-2004'
  climate_zone = 'ASHRAE 169-2006-1A'
  epw_file = 'Not Applicable'
  osm_directory = './'

  model = OpenStudio::Model::Model.new
  model.create_prototype_building(building_type,
                                template,
                                climate_zone,
                                epw_file,
                                osm_directory,
                                @debug)
end


# test()