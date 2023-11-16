 export let NearbyShelters =`<osm-script bbox="51.477,-0.001,51.55,0.081" output="json" output-config="">
            <union into="_">
              <query into="_" type="node">
                <has-kv k="amenity" modv="" v="hospital"/>
              </query>
              <query into="_" type="node">
                <has-kv k="healthcare" modv="" v=""/>
              </query>
            </union>
            <print e="" from="_" geometry="skeleton" ids="yes" limit="" mode="skeleton" n="" order="id" s="" w=""/>
            <print e="" from="_" geometry="skeleton" ids="yes" limit="" mode="body" n="" order="id" s="" w=""/>
          </osm-script>`

