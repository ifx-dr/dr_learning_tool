BEGIN TRANSACTION;
CREATE TABLE ontology (
	id SERIAL, 
	name VARCHAR(150) NOT NULL, 
	description VARCHAR(10000), 
	image_url VARCHAR(255), 
	ontology_url VARCHAR(255), 
	PRIMARY KEY (id)
);
INSERT INTO ontology VALUES(DEFAULT,'Digital Reference','Holistic Ontology for semiconductor manufacturing and development, products and systems containing semiconductors and connected supply chains.','picture/ontologies_pictures/Lobesv1.png','DigitalReference.rdf');
INSERT INTO ontology VALUES(DEFAULT,'Planning Lobe','This Lobe models semiconductor supply chain planning','picture/ontologies_pictures/supplychain.jpg','PlanningOntology.rdf');
INSERT INTO ontology VALUES(DEFAULT,'Microcontroller','This ontology deals with the domain microcontroller.','picture/ontologies_pictures/microcontroller.jpg','microcontroller.rdf');
INSERT INTO ontology VALUES(DEFAULT,'Ordermanagement','This ontology deals with the domain order management.','picture/ontologies_pictures/OrderManagement.jpg','OrderManagement.rdf');
INSERT INTO ontology VALUES(DEFAULT,'Power','Power2Power is an European co-funded innovation project on Semiconductor Industry with the goal of conducting the research and development of innovative power semiconductors with more power density and energy efficiency','picture/ontologies_pictures/Power.jpg','Power.rdf');
INSERT INTO ontology VALUES(DEFAULT,'Sc Planning','This ontology represents how Infineon’s Supply Chain Planning works and which role deviations play in this process.','picture/ontologies_pictures/SC_Planning.jpg','SC_Planning.rdf');
INSERT INTO ontology VALUES(DEFAULT,'Sensor','This ontology deals with the domain sensor.','picture/ontologies_pictures/sensor.jpg','sensor.rdf');
INSERT INTO ontology VALUES(DEFAULT,'Supplychain','This ontology deals with the domain SupplyChain.','picture/ontologies_pictures/supplychain.jpg','supplychain.rdf');
INSERT INTO ontology VALUES(DEFAULT,'Your Ontology',NULL,'picture/ontologies_pictures/YOUR_ONTOLOGY.jpg','YOUR_ONTOLOGY.rdf');
CREATE TABLE department_ontology_association (
	id SERIAL, 
	department VARCHAR(150) NOT NULL, 
	ontology_id SERIAL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(ontology_id) REFERENCES ontology (id)
);
INSERT INTO department_ontology_association VALUES(DEFAULT,'CSC (Corporate Supply Chain)',DEFAULT);
INSERT INTO department_ontology_association VALUES(DEFAULT,'GIP (Green Industrial Power)',DEFAULT);
INSERT INTO department_ontology_association VALUES(DEFAULT,'PSS (Power & Sensor Systems)',DEFAULT);
INSERT INTO department_ontology_association VALUES(DEFAULT,'PSS (Power & Sensor Systems)',DEFAULT);
CREATE TABLE "user" (
	id SERIAL, 
	email VARCHAR(150), 
	password VARCHAR(150), 
	first_name VARCHAR(150), 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO "user" VALUES(DEFAULT,'nils@gmail.com','pbkdf2:sha256:600000$AQZjXuClZdWr7PRb$6d22cbeb17e2a776d29318ef9b71b2bac296c4033b13d78564cc3b5316a76332','Nils');
INSERT INTO "user" VALUES(DEFAULT,'tim@gmail.com','pbkdf2:sha256:600000$pZTTiAtqySeePd6E$f896c8dc3b0317099ab6d871bef00a701718eb8a3978228b74cc936d3e1cd031','Tim');
INSERT INTO "user" VALUES(DEFAULT,'marie@gmail.com','pbkdf2:sha256:600000$8DKqUWsppIDgXyOd$54de10d235243b01745a09c265a7fb4b551d79e172f35f6c9a88767b47a15de6','Marie');
INSERT INTO "user" VALUES(DEFAULT,'abcd@gmail.com','pbkdf2:sha256:600000$HuxL2dxHa3qQDZ0O$2b2d38b973a8575593ea6b72deba47f3eddd171116fae17cfb109b9a40881d24','Syha');
INSERT INTO "user" VALUES(DEFAULT,'jon.legorburu@infineon.com','pbkdf2:sha256:600000$zaesaVlpgSdBbxkt$9c3eb417dcc8e7d3a3b0befac2a8e685a4bbf22b13f500a5862d346e60418853','Jon');
INSERT INTO "user" VALUES(DEFAULT,'demo@demo','pbkdf2:sha256:600000$qL8kH4Lt3MkAqx2f$5a25aff6b42102a3a69a350467a38e2a86ea0e2e7f114329061ec3491984b4df','Demo');
INSERT INTO "user" VALUES(DEFAULT,'sc4eu@infineon.com','pbkdf2:sha256:600000$f6ea132839244c08de644b8e86916db7$ac1f241c8b03240c1b43f544fec9f2e10b754467ce396e91eef858ef9f7dcc1b','SC4EU');
CREATE TABLE profile (
	id SERIAL, 
	username VARCHAR(150), 
	profile_picture VARCHAR(150), 
	level INTEGER, 
	xp INTEGER, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "user" (id)
);
INSERT INTO profile VALUES(DEFAULT,'Nils','picture/user_profile/user2-removebg-preview.png',15,12660,1);
INSERT INTO profile VALUES(DEFAULT,'Tim','picture/user_profile/user1-removebg-preview.png',0,0,2);
INSERT INTO profile VALUES(DEFAULT,'Marie','picture/user_profile/user1-removebg-preview.png',0,24,3);
INSERT INTO profile VALUES(DEFAULT,'Syha','picture/user_profile/user1-removebg-preview.png',1,110,4);
INSERT INTO profile VALUES(DEFAULT,'Jon','picture/user_profile/user1-removebg-preview.png',0,0,1);
INSERT INTO profile VALUES(DEFAULT,'Demo','picture/user_profile/user1-removebg-preview.png',0,0,6);
INSERT INTO profile VALUES(DEFAULT,'SC4EU','picture/user_profile/user1-removebg-preview.png',0,99,7);
CREATE TABLE challenges (
	id SERIAL, 
	challenge VARCHAR(10000), 
	xp_reward INTEGER, 
	name VARCHAR(10000), 
	PRIMARY KEY (id)
);
CREATE TABLE user_challenges (
	id SERIAL, 
	user_id SERIAL, 
	challenge_id SERIAL, 
	completed BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES "user" (id), 
	FOREIGN KEY(challenge_id) REFERENCES challenges (id)
);
CREATE TABLE game_information (
	id SERIAL, 
	profile_id SERIAL, 
	department VARCHAR(150), 
	ontology_id INTEGER, 
	num_questions INTEGER, 
	random_word VARCHAR(150), 
	random_definition VARCHAR(10000), 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profile (id), 
	FOREIGN KEY(ontology_id) REFERENCES ontology (id)
);
INSERT INTO game_information VALUES(DEFAULT,DEFAULT,'CSC (Corporate Supply Chain)',3,5,'Supply','This is the total amount of specific products that is available to customers. Supply has the dimensions quantity, time, location, product, including aggregation of all dimensions. Supply is defined as inventory or plan replenishment.');
CREATE TABLE used_word (
	id SERIAL, 
	profile_id SERIAL, 
	word_uri VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profile (id)
);
INSERT INTO used_word VALUES(DEFAULT,DEFAULT,'http://www.w3id.org/ecsel-dr-OM#Customer_Data');
INSERT INTO used_word VALUES(DEFAULT,DEFAULT,'http://www.w3id.org/ecsel-dr-OM#Supply');
CREATE TABLE definition_scores (
	id SERIAL, 
	class_name VARCHAR(150), 
	definition VARCHAR(10000), 
	score FLOAT, 
	agreements INTEGER, 
	disagreements INTEGER, 
	latest_review INTEGER, 
	split_review BOOLEAN, 
	is_default BOOLEAN, 
	PRIMARY KEY (id)
);
INSERT INTO definition_scores VALUES(DEFAULT,'Order','An order signifies a formal request or instruction for the procurement, distribution, or delivery of products or services within the supply chain. It encompasses customer orders, replenishment orders, or split orders initiated to fulfill demand, replenish inventory, or redistribute products.',1.0,1,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Order','In the supply chain context, an order represents a formal directive or request for the acquisition, distribution, or movement of products or services. It includes customer orders, replenishment orders, or split orders issued to meet demand, manage inventory, or facilitate product allocation.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Customer','A customer represents an individual, organization, or entity that purchases or engages with products or services offered within the supply chain. It encompasses buyers, end-users, retailers, or entities procuring goods or services within the supply chain network.',2.1000000000000000888,2,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Customer','In the supply chain context, a customer signifies an individual, organization, or entity that procures, consumes, or engages with products or services. It includes wholesalers, retailers, end-users, or entities involved in the procurement and consumption of goods within the supply chain.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Customer','Customers (or consumers) are individuals or organizations that purchase and use a product or service. A customer may be an organization (a producer or distributor) that purchases a product in order to incorporate it into another product that they in turn sell to their customers (ultimate customers).',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'CustomerPlant','A customer plant denotes a physical location, facility, or entity operated by a customer within the supply chain. It encompasses distribution centers, manufacturing facilities, or operational sites managed by customers to facilitate order fulfillment and product management.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'CustomerPlant','Within the supply chain, a customer plant represents a specific facility, warehouse, or operational site managed by a customer to handle order receipt, inventory management, and product distribution. It includes distribution centers, manufacturing plants, or fulfillment hubs operated by customers.',2.1000000000000000888,2,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Product','A product refers to a physical item or service that is available for purchase, distribution, or utilization within the supply chain. It encompasses merchandise, parts, or services that are produced, exchanged, or utilized within the network of the supply chain.',0.0,1,1,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Product','A product represents a tangible item or service offered for sale, distribution, or use within the supply chain. It encompasses goods, components, or services that are manufactured, traded, or consumed within the supply chain network.',1.0,1,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Product','In the context of the supply chain, a product refers to a distinct item, part, or service involved in manufacturing, distribution, or consumption processes. It includes physical goods, components, or services that are integral to supply chain operations and customer fulfillment.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'ReplenishmentOrder','A replenishment order signifies a directive for the resupply or replenishment of products or inventory within the supply chain. It encompasses orders initiated by customer plants, distribution centers, or manufacturers to replenish stock, manage inventory levels, or fulfill supply chain requirements.',1.0,1,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'ReplenishmentOrder','Within the supply chain, a replenishment order represents a formal instruction for restocking, refilling, or replenishing inventory levels. It includes orders issued by customer plants, distribution centers, or manufacturers to maintain adequate stock, manage inventory, or meet supply chain demands.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'CustomerOrder','A customer order represents a specific request placed by a customer for the procurement of products or services. It encompasses orders initiated by customers to fulfill demand, replenish inventory, or acquire goods for consumption or resale within the supply chain network.',1.0,1,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'CustomerOrder','In the supply chain context, a customer order denotes a formal request placed by a customer for the acquisition of products or services. It includes orders initiated by customers to meet demand, manage inventory, or fulfill procurement requirements within the supply chain.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'SplitOrder','A split order denotes a customized directive for the division or allocation of products or services into multiple segments or destinations within the supply chain. It encompasses tailored orders designed to distribute or allocate products to specific recipients, locations, or channels based on customized requirements.',1.0,1,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'SplitOrder','In the supply chain context, a split order represents a specialized instruction for the partitioning, segregation, or allocation of products into distinct segments or destinations. It includes customized orders tailored to distribute or allocate products to specific recipients, locations, or channels based on specific requirements.',1.9859999999999997655,3,1,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Microcontroller','A microcontroller is a programmable device that integrates a processor, memory, and input/output interfaces to control and interact with external devices and systems.',1.0,1,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Microcontroller','A microcontroller is a small computer on a single integrated circuit (IC) that contains a processor, memory, and input/output peripherals.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Microcontroller_Feature','A microcontroller feature is a hardware or software component of a microcontroller that enables it to perform a particular task or function, such as data conversion, communication, or control.',1.0,1,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Microcontroller_Feature','A microcontroller feature is a specific capability or functionality provided by a microcontroller, such as analog-to-digital conversion, serial communication, or pulse-width modulation.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Microcontroller_Application','A microcontroller application is a software or firmware program that runs on a microcontroller to control and interact with external devices, sensors, and actuators.',1.0,1,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Microcontroller_Application','A microcontroller application is a specific use case or project that utilizes a microcontroller to perform a particular function or set of functions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Analog-to-Digital_Converter','An analog-to-digital converter is a device that translates continuous analog signals into discrete digital values, allowing microcontrollers to read and process analog data.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Analog-to-Digital_Converter','An analog-to-digital converter is a microcontroller feature that converts analog signals from sensors or other devices into digital signals that can be processed by the microcontroller.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Embedded_System','An embedded system is a combination of computer hardware and software designed to perform a specific function or set of functions, often with real-time constraints.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Embedded_System','An embedded system is a microcontroller-based system that is integrated into a larger device or system, such as a consumer appliance, industrial machine, or automotive system.',1.0,1,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Industrial_Automation','Industrial automation refers to the use of control systems, such as microcontrollers and programmable logic controllers (PLCs), to monitor and control industrial processes and machinery.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Agent','The Agent class is the class of agents; things that do stuff. A well known sub-class is Person, representing people. Other kinds of agents include Organization and Group.\n\nThe Agent class is useful in a few places in FOAF where Person would have been overly specific. For example, the IM chat ID properties such as jabberID are typically associated with people, but sometimes belong to software bots.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'ObservationCollection','An Observation Collection has at least one member, and may have one of any of the other seven properties mentioned in restrictions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'TemporalEntity','A temporal interval or instant.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'SampleRelationship','Members of this class represent a relationship between a sample and another.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Deployment','Describes the Deployment of one or more Systems for a particular purpose. Deployment may be done on a Platform.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'System','System is a unit of abstraction for pieces of infrastructure that implement Procedures. A System may have components, its subsystems, which are other systems.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Stimulus','An event in the real world that ''triggers'' the Sensor. The properties associated to the Stimulus may be different to the eventual observed ObservableProperty. It is the event, not the object, that triggers the Sensor.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Property','A quality of an entity. An aspect of an entity that is intrinsic to and cannot exist without the entity.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Input','Any information that is provided to a Procedure for its use.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'OversamplingRate','Specifies the number of sensor measurements used internally to generate one sensor output result. (Oversampling rate = OSR)',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'OperatingRange','Describes normal OperatingProperties of a System under some specified Conditions. For example, to the power requirement or maintenance schedule of a System under a specified temperature range.\nIn the absence of OperatingProperties, it simply describes the Conditions in which a System is expected to operate.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'OperatingProperty','An identifiable characteristic that represents how the System operates under the specified Conditions. May describe power ranges, power sources, standard configurations, attachments and the like.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'SurvivalRange','Describes SurvivalProperties of a System under some specified Conditions. For example, the lifetime of a System under a specified temperature range.\nIn the absence of SurvivalProperties, simply describes the Conditions a System can be exposed to without damage. For example, the temperature range a System can withstand before being considered damaged.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'SurvivalProperty','An identifiable characteristic that represents the extent of the System''s useful life under the specified Conditions. May describe for example total battery life or number of recharges, or, for Sensors that are used only a fixed number of times, the number of Observations that can be made before the sensing capability is depleted.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'SystemCapability','Describes normal measurement, actuation, sampling properties such as accuracy, range, precision, etc. Of a System under some specified Conditions such as temperature range. The capabilities specified here are those that affect the primary purpose of the System, while those in OperatingRange represent the system''s normal operating environment, including Conditions that don''t affect the Observations or the Actuations.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'SystemProperty','An identifiable and observable characteristic that represents the system''s ability to operate its primary purpose: a sensor to make Observations, an Actuator to make Actuations, or a Sampler to make Sampling.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Condition','Used to specify ranges for qualities that act as Condition on a Systems'' operation.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'RelationshipNature','Nature of a relationship (between samples) - Members of this class indicate the nature of a relationship between two samples.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Accuracy','The closeness of agreement between the Result of an Observation (resp. The command of an Actuation) and the true value of the observed ObservableProperty (resp. Of the acted on ActuableProperty) under the defined Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'ActuationRange','The range of property values that can be the Result of an Actuation under the defined Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'BatteryLifetime','Total useful life of a System''s battery in the specified Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'DetectionLimit','An observed value for which the probability of falsely claiming the absence of a component in a material is beta, given a probability alpha of falsely claiming its presence.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Drift','As a Sensor Property: a continuous or incremental change in the reported values of Observations over time for an unchanging Property under the defined Conditions. As an Actuator Property: a continuous or incremental change in the true value of the acted on ActuableProperty over time for an unchanging command under the defined Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Frequency','The smallest possible time between one Observation, Actuation, or Sampling and the next, under the defined Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Latency','The time between a command for an Observation and the Sensor providing a Result, under the defined Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'MaintenanceSchedule','Schedule of maintenance for a System in the specified Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'MeasurementRange','The set of values that the Sensor can return as the Result of an Observation under the defined Conditions with the defined system properties.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'OperatingPowerRange','Power range in which System is expected to operate in the specified.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Precision','As a sensor capability: The closeness of agreement between replicate Observations on an unchanged or similar quality value: i.e., a measure of a Sensor''s ability to consistently reproduce an Observation, under the defined Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Resolution','As an actuator capability: The closeness of agreement between replicate Actuations for an unchanged or similar command: i.e., a measure of an Actuator''s ability to consistently reproduce an Actuations, under the defined Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'ResponseTime','As a Sensor Property: the time between a (step) change in the value of an observed ObservableProperty and a Sensor (possibly with specified error) ''settling'' on an observed value, under the defined Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Selectivity','As an Actuator Property: the time between a (step) change in the command of an Actuator and the ''settling'' of the value of the acted on ActuatableProperty, under the defined Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Sensitivity','As a Sensor Property: Sensitivity is the quotient of the change in a Result of Observations and the corresponding change in a value of an ObservableProperty being observed, under the defined Conditions.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'SystemLifetime','The System continues to operate as defined using SystemCapability. If, however, the SurvivalRange is violated, the System is ''damaged'' and SystemCapability specifications may no longer hold.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Management_System','A battery management system is, according to Infineon´s definition, a set of "electronic control circuits that monitor and regulate the charging and discharge of batteries." It supervises parameters such as the temperature, voltages, capacity, state of charge, power consumption, charging cycles. (Source: https://www.infineon.com/cms/en/applications/solutions/battery-management-system/ )\n\nAccording to VDMA and RWTH Aachen, the Battery Management System controls the cooling system, the slave PCBs of the battery modules, and the high voltage system.\n\nThese two definitions are compatible, as the first one determines the purpose of the BMS, and the second one the control hierarchy.\n\nBMS consist of one BMS master module which is a physcial part of the battery pack (beside the battery modules) and a set of BMS slave modules, one in each battery module.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_CO2_Savings_Enabler','CO2 Savings refers to several solutions that might reduce carbon emissions throughout the course of a Lithiu-Ion battery''s lifespan.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_CO2_Savings_Enabler','HB (2023-06-25): \n\nI renamed this class to ..._Enabler, as subclasses like longer lifespan enable CO2 savings, but they are not CO2 savings themselves. \n\nThe class hierarchy is an "isA"-Hierarchy: so every element of a subclass is automatically also an element of the superclass. \n\nFor this reason, I also removed the object property enables_CO2_saving, as the intention of this object property is already fulfilled by the class hierarchy here. \n\nFurthermore, I introduced a new class Transportation_CO2_Savings_Enabler and moved the subclass Electric_Means_Transportation to this class. The justification for this is that electric means transportation is very different from the battery CO2 savings enablers.\n\nThe whole topic of modelling CO2 savings in the context of e-Mobility needs to be further discussed!',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'BMS_Constructive_Block','A Battery Management System consists of a BMS master which is a physical part of the battery pack (outside and different from the battery modules) and BMS slaves, which are part of battery modules. \nThat is, a BMS of a battery pack consists of one BMS master and N BMS slaves where N is the number of battery modules of the battery pack.\n\nThe constructive decomposition needs to be treates separately from the functional decomposition (functional blocks).',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'BMS_Functional_Block','A Functional Block is a component of the battery management system.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Vehicle','A vehicle is a machine with wheels and an engine, used for transporting people or goods.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'BatteryManagementSystem_Company','https://nuvationenergy.com/battery-management-systems/',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Module','A battery module contains several battery cells. \nA battery pack contains several battery modules and a BMS (and further components).',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Cell','Cells are fundamental electrochemical unit, or assembly of electrodes, separators, electrolyte, container, and terminals, that serves as a source of electrical energy by directly converting chemical energy. In this case, the cells are all of the type Li-Ion.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Pack','A battery pack is a set of battery modules, a BMS and several further components.\nThe main components of a battery pack are:\n- battery modules, including a BMS slave each\n- high-voltage module\n- Battery Management System Master \n- cooling system\n- wiring \n\nA battery pack has three main interfaces to outside systems: \n- coolant connection\n- CAN interface\n- Service Plug and Power Supply.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Traction_Battery','Traction Batteries are car batteries with high voltage, that supply the electric traction motors of e-cars. \nHence, traction batteries are both car batteries and high voltage batteries. This leads inevitably to a multiple inheritance situation for this class.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Cooling_System','A battery cooling system is part of a battery pack. Its purpose is to cool, but also to heat if needed, the battery modules in the battery pack.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Semiconductor','Semiconductor is an eletronic device which electrical conductivity value is between an insulator and a conductor. In this case, constitutes the battery management system.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Voltage_Class','The voltage class is the most important property of batteries. It is often used to separate batteries into different classes, like HV battery for High Voltage battery. Hence, the voltage classes are modelled in this ontology explicitely.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_High_Voltage_System','A battery high voltage system is part of a battery pack. \nIt consists of relay, fuses, pre-charge and current measuring system, insulation monitoring etc.\n\nThe High-voltage system and the BMS are different entities, both physically and regarding their functionality. \nHowever, there seem to exist strong interdependencies between these systems. \nAccording to VDMA and RWTH Aachen the BMS controls the high-voltage system. \n\nAnd, it seems that also the high-voltage system contains semiconductors!!',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ferrophosphate_Battery_Management_System','Full name: Lithium-Ferrophosphate Battery Management System',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ferrophosphate_Battery_Cell','Battery cell of Lithium-Ferrophosphate batteries. \n\nThe cathodes of LiFePO4 batteries consist of Lithium-Ferrophosphate.\n\nTypical cell currency is 3.2 to 3.3 Volt.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'LFP_Traction_Battery','LFP batteries are not so widely used as traction batteries of cars as traditional Li-Ion batteries or Lithium-Polymere batteries. \nThe main disadvantage of LFP batteries is the lower cell voltage of 3.2 to 3.3 Volt compared to 3.6 V of Li-Ion cells with Lithium-Cobalt basis and 3.7 V of Lithium-Polymere cells). \nBut they have significant advantages in terms of safety, as they cannot come into a thermic interference ("thermisches Durchgehen") and hence cannot start to burn from thereselves. \n\nTesla tested LFP traction batteries for its Model 3, and BYD started to use them widely. BYD produces LFP cells by themselves. They also offer the first E-bus with LFP traction battery.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ion_Battery_Cell','The base technology in Lithium-Ion cells are cathods from Lithium-Cobalt(III)-Oxid (LiCoO2).\n\nTypical cell currency is 3.6 Volt.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ion_Traction_Battery','A Lithium-Ion traction battery of an e-car is both a traction battery and a Lithium-Ion battery. \nHence, this class is subclass of two different classes, on the one hand of a car battery and on the other hand of a battery type. \nSo it inherits properties from the "purpose" class as well as of the "type" class.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Semiconductor_Company','Company responsible for the manufacturing of semiconductors.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Voltage_Class','Class that allows to classify batteries according to their voltage. Most important sub class is High Voltage Battery (HV battery). But there are low voltage batteries as well.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ferrophosphate_Battery','Lithium-Eisenphosphat-Batterien (LiFePO4):\nDie vielen technischen Vorteile der innovativen Lithium-Technologie waren bislang meist nur bei Versorgungsbatterien zu finden, so zum Beispiel auch bei der Traction-LFP-Serie von Accurat. Mit der Accurat Impulse LFP nutzen Sie diese innovative Technologie nun auch als Starterbatterie für ihr Fahrzeug.\n\nDie Lithium-Eisenphosphat-Batterien, kurz LiFePO4 oder LFP genannt, gelten als die sichersten Lithium-Batterien und setzen neue Maßstäbe im Bereich der Starterbatterien. In Standard-Batteriegehäusen sind diese Batterien sofort einsatzbereit und 1:1 gegen herkömmliche Blei-, EFB- oder AGM-Batterien austauschbar.\n\nDer extrem geringe Innenwiderstand der LFP-Batterien bewirkt eine einzigartige Hochstromfähigkeit. Hierdurch kann die Lichtmaschine ihres Fahrzeugs die Batterie in kürzerer Zeit mit deutlich höheren Strömen aufladen.\n\nOb Leistungsabgabe, Ausdauer, Schnellladefähigkeit, Gewicht oder Kapazität – eine Accurat Impulse LFP punktet mit vielen technischen Vorzügen, die eine zuverlässige Stromversorgung garantieren.\n\nAccurat Impulse Batterien mit LFP-Technologie überzeugen mit ihrer Leistung, Gewicht – und Sicherheit. Dank ihrer Bauart und dem intelligenten Batterie-Management-System (BMS) sind alle Modelle geschützt vor Überladung, Kurzschluss und Überhitzung. Lithium-Batterien können Sie so überall problemlos verbauen – auch bei Umgebungstemperaturen von über 50 °C. Und dank ihrer geringen Selbstentladung lassen Sie sich ganz einfach lagern – garantiert ohne Gasung.\n\nSource: Accurat (https://www.autobatterienbilliger.de/Accurat-Impulse-I20L3-Lithium-Autobatterie-20Ah-LiFePO4)',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ion_Battery','A Lithium-Ion Battery consists of a set of battery packs and a battery management system.\n\nThe base technology in Lithium-Ion batteries are Lithium-Ion cells with Lithium-Cobalt(III)-Oxid (LiCoO2).',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Absorbant_Glass_Mat_Battery','The AGM battery is versatile, powerful and designed for high demands. At its core, the structure of an AGM is no different from that of a wet battery. However, the electrolyte in an AGM is no longer free-floating but bound in a special glass fiber separator - hence the name "absorbent glass mat". The large contact area achieved in this way contributes to the high power output and also makes the battery leak-proof. Due to its design, the battery is hermetically sealed. This special feature enables the internal recombination of oxygen and hydrogen, so that there is no loss of water. To protect against impermissible overpressure, the individual battery cells are equipped with a safety overpressure valve, so that safety is guaranteed even in the event of a fault.\n\nThe AGM battery also has significant advantages over simple starter batteries in terms of service life. An AGM battery can handle three times as many charging cycles as a conventional starter battery. Another advantage of the AGM battery is that it is position-independent, since the material integration of the electrolyte means that no liquid can leak out. Even if the battery housing breaks, no battery acid can leak out.\n\nAn AGM battery is the ideal energy storage system for vehicles with automatic start-stop systems with braking energy recovery (recuperation), since a conventional starter battery cannot meet the high performance requirements of these systems. But the AGM battery is also the right choice for cars that have a high energy demand and a large number of electrical consumers on board.\n\nSource: Varta (https://batteryworld.varta-automotive.com/de-de/batterietypen-sli-efb-agm-unterschiede)',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'BMS_Slave_Module','A BMS slave module is physical part of a battery module and logically part of the Battery Management System of the battery pack. \nThe BMS consists of one BMS master and one BMS slave for each battery module.\n\nA BMS slave can either consist of a slave circuit board and several temperature and voltage sensors and a contacting unit, \nor can be a completely integrated system. The latter is modeled in this ontology as class Semiconductor - Multichannel_Battery_Monitoring_IC with an Infineon product as instance.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Enhanced_Flooded_Battery','Die EFB-Batterie – viele Ladezyklen und lange Lebensdauer\n\nDie EFB-Batterie ist eine optimierte und leistungsgesteigerte Version der Nassbatterie. Das Kürzel „EFB“ steht für „enhanced flooded battery“. Auch hier sind die Platten mit einem mikroporösen Separator voneinander isoliert. Zwischen Platte und Separator befindet sich zudem ein Polyester-Scrim. Dieses Material hilft, das aktive Material der Platten zu stabilisieren und die Lebensdauer der Batterie zu verlängern. Die EFB-Batterie überzeugt durch eine hohe Zahl an möglichen Ladezyklen und bietet mehr als doppelt so hohe Teilentladungs- und Tiefentladungsleistung im Vergleich mit konventionellen Batterien.\n\nOft wird die EFB-Batterie in Fahrzeugen mit einfacher Start-Stopp-Automatik verbaut. Aufgrund der überlegenen Leistung wird aber auch vermehrt beim Ersatz der herkömmlichen Blei-Säure zu einer Batterie mit EFB-Technologie gegriffen.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Enhanced_Flooded_Battery','Enhanced Flooded Batteries (EFB) are optimized and power-enhanced versions of SLI batteries.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Nickel_Metal_Hydride_Accumulator','Nickel_Metal_Hydride_Accumulator',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Lead_Acid_Battery','Lead-Acid-Batteries (Blei-Säure-Batterien) are traditional car onboard electronics batteries. \nThey are included in this ontology just as a second battery type different from Lithium-Ion batteries.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Starting_Lighting_Ignition_Battery','Die Nassbatterie (SLI) – bewährt und wirtschaftlich\n\nEine konventionelle Starterbatterie besteht aus sechs Batteriezellen. Eine Batteriezelle, auch Plattenblock genannt, besteht aus einem positiven und einem negativen Plattensatz, die wiederum aus mehreren Elektroden bestehen.\nEine positive Elektrode setzt sich aus aktiver Masse aus Bleioxid und einem positiven Gitter aus einer Bleilegierung zusammen. Die Gittergerüste verleihen den Elektroden eine solide Struktur und dienen gleichzeitig als Stromleiter. Die aktive Masse ist in einen Elektrolyt, ein Gemisch aus Säure und destilliertem Wasser, getaucht.\nEine negative Elektrode setzt sich ebenfalls aus aktiver Masse, hier jedoch bestehend aus purem Blei, und einem negativen Gitter zusammen. Getrennt werden die Elektroden unterschiedlicher Ladung von einem Separator. Durch eine Parallelschaltung der einzelnen Platten in den Zellen wird die benötigte Kapazität einer Batterie erreicht. Aus der Reihenschaltung der einzelnen Zellen ergibt sich die benötigte Spannungsladung von 12 Volt.\n\nHerkömmliche Batterien, wie Blei-Säure-Batterien, gehören zur gängigsten Batterietype. Diese Technologie wird häufig als SLI bezeichnet, was auf die Hauptaufgabe einer Batterie im Fahrzeug zurückgeht: Starting, Lighting, Ignition (Start, Licht, Zündung). Sie eigenen sich für Fahrzeuge ohne Start-Stopp-Technologie und einer moderaten Anzahl von elektrischen Verbrauchern.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Starting_Lighting_Ignition_Battery','SLI- (Starting, Lighting, Ignition) Batteries are the simplest types of car batteries. They are appropriate for cars without start-stopp technology and with low to medium number of electronic consumers.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Longer_Lifespan','Longer life cycle refers to the number of extra cycles of the battery due good handling throught its lifecycle. It is a way of CO2 savings.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Optimized_Charging','Second life means that the Lithium-Ion battery has ceased its main activity, in this case powering an electric car, however, it is still able to be used for other purposes.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Pouch_Cell_Battery_Module_Type','It is important to note that the pouch cells expands/shrinks in its thickness during the charging or discharging cycle.\n● Each pouch cell is inserted into a frame.\n● Due to the swelling of the cells, the frames are arrested flexible by springs.\n● Cooling in a pouch module is optional and can be served by either convective or liquid coolant.\n● For example, pouch cells can be serial connected and cooled via U-profiles.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Prismatic_Cell_Battery_Module_Type','Prismatic cells can be installed without remaining gaps.\n● The individual cells are glued together.\n● The adhesive film serves both as electrical and thermal insulator in the event of an accident.\n● The cells are clamped with a bandage and/or a plastic or metal housing.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Round_Cell_Battery_Module_Type','In the architecture of a round cell module, the cells are fixed by the module case.\n● The space between the cells can be used by a cooling system or direct cooling.\n● The metal housing prevents the cell from swelling.\n● At module level, the cells can be connected both serial and parallel.\n● The cells are contacted via a metal plate on both sides.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Trolley_Bus','A trolleybus (also known as trolley bus, trolley coach, trackless trolley, trackless tram – in the 1910s and 1920s[1] – or trolley[2][3]) is an electric bus that draws power from dual overhead wires (generally suspended from roadside posts) using spring-loaded trolley poles. Two wires, and two trolley poles, are required to complete the electrical circuit. This differs from a tram or streetcar, which normally uses the track as the return path, needing only one wire and one pole (or pantograph). They are also distinct from other kinds of electric buses, which usually rely on batteries. Power is most commonly supplied as 600-volt direct current, but there are exceptions.\n\nCurrently, around 300 trolleybus systems are in operation, in cities and towns in 43 countries.[4] Altogether, more than 800 trolleybus systems have existed, but not more than about 400 concurrently',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Infineon_Device','Should defined as its function for example:\n\n-Sensor\n-Power Converter \n-Microcontroller \n\nThen must be defined what the device it is, for exmaple:\n-A sensing device is a device that implments sensing.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'The_method_of_the_device_function','The function of the devices has a method ( Procedure to estimate or calculate a value), for example:\nThe Senor its function is the sensing, the sensing method is the observation\nThe Boost converter ( a type of the power converter) its function is boosting, the boosting method is the amplification.  \n\nAct of carrying out an (the method) Procedure to estimate or calculate a value of a property of a FeatureOfInterest. Links to an the methodProperty to describe what the result is an estimate of, and to a FeatureOfInterest to detail what that proeprty was associated with.\n\nExample: The activity of estimating the intensity of an earthquake using the Mercalli intensity scale is an Observation as is measuring the moment magnitude, i.e., the energy released by said earthquake.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Products','The superclass of all classes describing products or services types, either by nature or purpose. Examples for such subclasses are "TV set", "vacuum cleaner", etc. An instance of this class can be either an actual product or service (gr:Individual), a placeholder instance for unknown instances of a mass-produced commodity (gr:SomeItems), or a model / prototype specification (gr:ProductOrServiceModel). When in doubt, use gr:SomeItems.\n\nExamples: \na) MyCellphone123, i.e. my personal, tangible cell phone (gr:Individual)\nb) Siemens1234, i.e. the Siemens cell phone make and model 1234 (gr:ProductOrServiceModel)\nc) dummyCellPhone123 as a placeholder for actual instances of a certain kind of cell phones (gr:SomeItems)',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'GeometricDimension','"Describes the Dimensions of any Physical Object (Length, Wisth, Height)"',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'ApplicationArea','The different application ares that the product can be used.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Control_Method','It is the method used to turn on, turn off , increaseing, and decreasing output current/voltage.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'SiC_MOSFET','Silicon Carbide Metal Oxide Semiconductor Field Effect Transistor (SiC MOSFET): It is a transistor: It is used for switching or amplifying the electronics signals or electric power.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'System','System is a unit of abstraction for pieces of infrastructure that implements procedure. A System may have components, its subsystems, which are other systems."',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Deployment','The ongoing Process of Entities (for the purposes of this ontology, mainly the Infineon device) deployed for a particular purpose. For example, a particular Sensor deployed on a Platform, or a whole network of Sensors deployed for an observation campaign. The deployment may have sub processes, such as installation, maintenance, addition, and decomissioning and removal.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Process','A process has an output and possibly inputs, and for a compositive process, describes the temporal and dataflow dependencies and relationships amongst its parts.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Process_Input','Any information that is provided a Procedure for its use.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Platform','An Entity to which other Entities can be attached - particularly semiconductor products and other platforms.\n\nExample: A post might act as the platform, a body might act as a platform for an attached device.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'TheDeviceOutput','the device output is a piece of information (value), the value itself being represented by an The device function value.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Device','A device is a physical piece of technology - a system in a box. Devices may of course be build of smaller devices and software components."',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Situation','A view, consistent with (''satisfying'') a Description, on a set of entities. It can also be seen as a ''relational context'' created by an observer on the basis of a ''frame'' (i.e. a Description). For example, a PlanExecution is a context including some actions executed by agents according to certain parameters and expected tasks to be achieved from a Plan; a DiagnosedSituation is a context of observed entities that is interpreted on the basis of a Diagnosis, etc. Situation is also able to represent reified n-ary relations, where isSettingFor is the top-level relation for all binary projections of the n-ary relation. If used in a transformation pattern for n-ary relations, the designer should take care of creating only one subclass of Situation for each n-ary relation, otherwise the ''identification constraint'' (Calvanese et al., IJCAI 2001) could be violated.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Information_Object','A piece of information, such as a musical composition, a text, a word, a picture, independently from how it is concretely realized.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Quality','Any aspect of an Entity (but not a part of it), which cannot exist without that Entity. For example, the way the surface of a specific PhysicalObject looks like is a Quality, while the encoding of that Quality into e.g. a PhysicalAttribute should be modeled as a Region. From the design viewpoint, the Quality-Region distinction is useful only when individual aspects of an Entity are considered in a domain of discourse. For example, in an automotive context, it would be irrelevant to consider the aspects of car windows for a specific car, unless the factory wants to check a specific window against design parameters (anomaly detection). On the other hand, in an antiques context, the individual aspects for a specific piece of furniture are a major focus of attention, and may constitute the actual added value, because the design parameters for old furniture are often not fixed, and may not be viewed as ''anomalies''.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Documents','The document class presents those things which are, broadly conceived, "documents''''. It should contain the manuals and the data sheet of the devices.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Deployment-related_Process','Place to group all the various Processes related to Deployment. For example, as well as Deployment, installation, maintenance, deployment of the further devices and the like would all be classified under DeploymentRelatedProcess.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Abstract','Any Entity that cannot be located in space-time.\n\nExample: mathematical entities: formal semantics elements, regions within dimensional spaces, etc.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Entity','Anything: real, possible, or imaginary, which some modeller wants to talk about for some purpose.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'IndutrialSector','The collection of all localized groups of enterprises that are producers of industrial commodities, in which each such group together forms the major industrial sector for the region. ''Industrial commodities'' includes MechanicalDevices and basic industrial materials. Examples include ''the world industrial sector'', the ''industrial sector of China''. The Chinese water pump industry would not be an exemplar of IndustrialEconomicSector but would rather be a sub-industry (see subIndustries) of it. On the other hand, chinese water pump manufacturers would be considered groupMembers of ''the industrial sector of China''.\n\nThis classification is done by The Global Industry Classification Standard (GICS) is an industry taxonomy developed in 1999 by MSCI and Standard & Poor''s (S&P) for use by the global financial community. The GICS structure consists of 11 sectors, 24 industry groups, 68 industries and 157 sub-industries[1] into which S&P has categorized all major public companies',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Interface','A common boundary or interconnection between systems, equipment, concepts, or human beings',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Object','Any physical, social, or mental object, or a substance',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Package','A package is the housing for a chip (or several chips) and provides electrical contacts. It is an interconnect in between chip-pads and the interface to the PCB board. A package is characterized by its outline (drawing) and its materials.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Social_Object','Act of carrying out an (Observation) Procedure to estimate or calculate a value of a property of a FeatureOfInterest. Links to an ObservableProperty to describe what the result is an estimate of, and to a FeatureOfInterest to detail what that proeprty was associated with.\n\nExample: The activity of estimating the intensity of an earthquake using the Mercalli intensity scale is an Observation as is measuring the moment magnitude, i.e., the energy released by said earthquake.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'SwitchingValue','The value of the result of the method (procedures) of the device function. The result is an information object that encodes some value for a feature. \nFor example:\n-If we consider the observation is the method used for sensing of the sensors, then the observation has a result which is the output of the sensor,\n-If -If we consider the amplification is the method used for boosting of the power converter, then the amplification has a result which is the output of the  power converter,',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'The_process_name_of_the_device_function','It is a process that results in the estimation, or calculation, of the value of a device output. \nUsually it derived from the name of the device for example:\nSensor process: sensing: Sensing is a process that results in the estimation, or calculation, of the value of a phenomenon.\n\nBoost Converter process: boosting: is a process that results in the estimation, or calculation, of the value of a amplified voltage.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Allocation','Allocation is a process used in order management in times when demand exceeds available supply.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Supply','This is the total amount of specific products that is available to customers. Supply has the dimensions quantity, time, location, product, including aggregation of all dimensions. Supply is defined as inventory or plan replenishment.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Order_Confirmation','A notification  that an order has been received and accepted',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Open_Order','An order that has been placed, but not yet fulfilled or completed',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Order_Line_Item','A single item  that is part of a larger order. It represents a specific product or service that a customer has ordered, along with its associated details.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Open_Order_Book','A continuously updated  record of all outstanding sell orders',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Contact_Person_Data','Data of the contact person',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Customer_Data','Customer data such as address and company name',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Supplier_Data','Data about the supplier such as name, location, address',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Customer','A customer is an business that purchases another company''s goods or services.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Customer_Plant','Manufacturing site where the cusomer procuces goods',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Supplier','A supplier is a company or organization that provides goods, services, or materials to another entity',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Order_Change_Request','A request to modify an existing order that has not yet been fulfilled',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Action','The process of doing something',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'UserAction','Activity taken by user',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Demand_Fulfillment','The process of meeting a customer’s demand for product or services by fulfilling their request.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Customer_Data','My new definition',1.0,1,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Car_Battery','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'BatteryCell_Company','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Module_Housing','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Module_Company','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'High_Voltage_Battery','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Pack_Housing','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Pack_Company','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Company','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Type','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Current_Sensing','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Current_Sensor','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'High_Voltage_Class','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Onboard_Electronics_Network_Battery','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Low_Voltage_Class','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Pack_HV_System_Component','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ferrophosphate_Battery_Module','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ferrophosphate_Battery_Pack','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Li-Ion_Battery_Management_System','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Li-Ion_Battery_Module','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ion_Battery_Pack','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ion_High_Voltage_Battery','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Control_Unit','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Cell_Supervision','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Multichannel_Battery_Monitoring_Integrated_Circuit','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Pack_Monitoring','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Multichannel_Controller_Integrated_Circuit','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Power_Management_Integrated_Circuit','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Pressure_Sensor','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Electric_Vehicle','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Electric_Passenger_Car','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Isolated_Communication','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'UART_Transceiver_Integrated_Circuit','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Car_Company','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Module_Construction_Type','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Industrial_Company','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Transportation_CO2_Savings_Enabler','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Nickel_Cadmium_Accumulator','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'BMS_Master_Module','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Electric_Bus','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Electric_Bus','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Battery_Electric_Truck','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Electric_Truck','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Conventional_Bus','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Conventional_Vehicle','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Conventional_Light_Commercial_Vehicle','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Conventional_Passenger_Car','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Conventional_Truck','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Current_Measuring_System','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Electric_Means_Transportation','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Fuel_Cell_Electric_Bus','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Fuel_Cell_Electric_Car','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Fully_Electric_Car','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Plugin_Hybrid_Car','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Fuel_Cell_Electric_Truck','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Fuse','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Insulation_Monitoring','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'LFP_BMS_Master_Module','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'LFP_BMS_Slave_Module','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'LFP_Onboard_Electronics_Battery','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Lead_Acid_Onboard_Electronics_Battery','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Li-Ion_BMS_Master_Module','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Li-Ion_BMS_Slave_Module','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ferrophosphate_High_Voltage_Battery','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Lithium-Ion_Onboard_Electronics_Battery','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Pre_Charge_Measuring_System','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Relay','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Trolley_Truck','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Serial_Peripheral_Interface','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Customer_Plant_Data','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'The_Application_Voltage','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Drain_Voltagea','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Depletion_Mode','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Variable_Resistance','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'On-State_Power_loss','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'DrainCurrent','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'On-State_Resistance','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Enhancement','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Switcher','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Maximum_Junction_Temperature','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Semiconductors','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Device_Configuration','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Device_Elements','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'SemiconductorProduct(its_name)_DataSheet','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'On-State_Voltage','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Threshold_Voltage','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Region_of_Operation','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Process_Output','Any information that is reported from a Procedure.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Operation_Mode','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Resistance','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Junction_Temperature','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Semiconductors&SemiconductorEquipment','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'N-Channel_Configuration','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Postive_(+)','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'P-channel_Configuration','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Negative_(-)','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Operating_Property','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Physical_Object','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Blocking_Capability','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Blocking_Voltage','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'CommunicationServices','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Constant_Resistance','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'ConsumerDiscretionary','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'ConsumerStaples','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'InformationEntity','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Drain','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Drain-Source_Voltage','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Electric_Vehicle_Charging','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'ElectronicComponents','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'ElectronicEquipment,Instruments&Components','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'TechnologyHardware&Equipment','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Energy','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Energy_Storage','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Financial','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Gate','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'GateDriver','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Healthcare','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Height','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Industrials','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'InformationTechnology','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Leakage_Current','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Length','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Materials','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Microcontroller','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Off-State_Region','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'On-State_Region','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Voltage','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'PowerConverters','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Price','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'RealEstate','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Saturation_Region','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Triode/Constant_Resistance_Region','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Sensors','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Solar_Energy','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Source','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Switching_Frequency','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Utilities','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Voltage-Controlled','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Weight','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Width','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Software&Services','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'SupplyDemandMatch','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'SupplyPicture','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'OrdersReschedule','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'MarketingDemands','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'SalesDemands','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'OrderLineItem','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'OpenOrderBook','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Orders','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'ATP','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'PrioritizedOrders','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'CLM','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'TargetAllocation','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'AATP','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'ordersScheduleLine','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Stocks','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'OperationalDemand','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Forecast','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Customers','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'nEWs','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'CapacityBottleneck','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'PrioritizedDemand','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'AggregatedCapacity','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Promise','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'BottleneckResource','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Confirmation','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'ResourceCapacity','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'AP_FCST','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'BufferStockOrders','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'ConsignmentOrders','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'DB','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'DC','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'EDIForecast','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'GeneralCustomers','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'HP_Forecast','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'MaxStock','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'SSO_Stocks','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'MinStock','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'NP_Forecast','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'OP_Forecast','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'PrivateCustomers','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'RampUpStock','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'RetainedStock','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'SafetyStock','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'StandardOrders','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'WIP','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Observation','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Actuation','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Sampling','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Output','Any information that is reported from a Procedure.',0.0,0,0,0,false,false);
INSERT INTO definition_scores VALUES(DEFAULT,'Vocabulary','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'SupplyChain','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'Sensor','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'TemperatureSensor','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'InfraredTemperatureSensor','No definition available',0.0,0,0,0,false,true);
INSERT INTO definition_scores VALUES(DEFAULT,'ThermocoupleTemperatureSensor','No definition available',0.0,0,0,0,false,true);
CREATE TABLE user_definitions (
	id SERIAL, 
	profile_id SERIAL, 
	profile_class VARCHAR(150), 
	profile_definition VARCHAR(10000), 
	action_type VARCHAR(50), 
	revised_definition VARCHAR(10000), 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profile (id) ON DELETE CASCADE 
	--FOREIGN KEY(profile_class) REFERENCES definition_scores (class_name) ON DELETE CASCADE, 
	--FOREIGN KEY(profile_definition) REFERENCES definition_scores (definition) ON DELETE CASCADE, 
	--FOREIGN KEY(revised_definition) REFERENCES definition_scores (definition) ON DELETE CASCADE
);
INSERT INTO user_definitions VALUES(DEFAULT,DEFAULT,'Customer_Data','Customer data such as address and company name','entered','My new definition');
CREATE TABLE extended_user_definitions (
	id SERIAL, 
	profile_id SERIAL, 
	profile_class VARCHAR(150), 
	profile_definition VARCHAR(10000), 
	action_type VARCHAR(50), 
	revised_definition VARCHAR(10000), 
	alternative_name VARCHAR(100), 
	abbreviation VARCHAR(100), 
	--german_name VARCHAR(100), 
	example VARCHAR(10000), 
	ontology_iri VARCHAR(250), 
	PRIMARY KEY (id), 
	FOREIGN KEY(profile_id) REFERENCES profile (id) 
	--FOREIGN KEY(profile_class) REFERENCES definition_scores (class_name), 
	--FOREIGN KEY(profile_definition) REFERENCES definition_scores (definition), 
	--FOREIGN KEY(revised_definition) REFERENCES definition_scores (definition)
);
INSERT INTO extended_user_definitions VALUES(DEFAULT,DEFAULT,'Customer_Data','Customer data such as address and company name','entered','My new definition','alternative name','abbreviation','Example','http://www.w3id.org/ecsel-dr-OM#');
COMMIT;